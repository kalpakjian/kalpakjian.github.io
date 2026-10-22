"""
train_cnn.py -- train the small CNN from the notes, on MNIST or CIFAR-10.

Why this differs from the notes' snippet:
  * Flatten -> Linear(64*8*8) hard-codes a 32x32 input. We end the conv trunk with
    AdaptiveAvgPool2d(1) (global average pooling) instead, so the SAME model definition
    works for 28x28 grayscale MNIST and 32x32 RGB CIFAR-10, at any resolution.
    5.7x fewer parameters too (545k -> 95k).
  * BatchNorm after every conv + bias=False: better conditioned, converges faster.
  * CIFAR-10 gets RandomCrop/HFlip augmentation (only 50k train images); MNIST gets
    RandomCrop only (flipping digits is harmful).

Run:
  set PY=C:\\Users\\princ\\miniconda3\\envs\\gpu\\python.exe
  %PY% C:\\Users\\princ\\cnn_demo\\train_cnn.py --dataset mnist   --epochs 3
  %PY% C:\\Users\\princ\\cnn_demo\\train_cnn.py --dataset cifar10 --epochs 20
  %PY% C:\\Users\\princ\\cnn_demo\\train_cnn.py --dataset mnist --epochs 1 --limit 2000 --dump-maps
"""
import argparse
import time
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms
from torchvision.utils import make_grid, save_image

DATASETS = {
    "cifar10": dict(
        cls=datasets.CIFAR10, in_ch=3, size=32, hflip=True,
        mean=(0.4914, 0.4822, 0.4465), std=(0.2470, 0.2435, 0.2616),
        classes=("plane", "car", "bird", "cat", "deer",
                 "dog", "frog", "horse", "ship", "truck"),
    ),
    "mnist": dict(
        cls=datasets.MNIST, in_ch=1, size=28, hflip=False,
        mean=(0.1307,), std=(0.3081,),
        classes=tuple("0123456789"),
    ),
}


class HFImageDataset(torch.utils.data.Dataset):
    r"""CIFAR-10 via HuggingFace `datasets`, used when the torchvision tarball is absent.

    The cine.cs.toronto.edu mirror is ~88 kB/s in this network (170 MB = 30+ min),
    while HF serves the same 50k/10k images in about a minute and caches them in
    %USERPROFILE%\.cache\huggingface, so subsequent runs are offline.
    """

    def __init__(self, split: str, transform):
        from datasets import load_dataset
        self.ds = load_dataset("uoft-cs/cifar10")[split]
        self.transform = transform
        self.targets = list(self.ds["label"])      # keeps the balanced `--limit` subset working

    def __len__(self) -> int:
        return len(self.ds)

    def __getitem__(self, i: int):
        row = self.ds[i]
        return self.transform(row["img"].convert("RGB")), int(row["label"])


def build_model(in_ch: int = 3, num_classes: int = 10, arch: str = "small") -> nn.Module:
    """Two capacities. `small` = the notes' model (95k params), `wide` = 4 blocks (1.5M).

    Both end with GAP so the same definition works for 28x28 and 32x32 inputs.
    The block sequence stays 0/2/4 = block1/2/3 in nn.Sequential, so the inspection
    helpers keep working for both architectures.
    """

    def block(cin: int, cout: int) -> nn.Sequential:
        return nn.Sequential(
            nn.Conv2d(cin, cout, 3, padding=1, bias=False),
            nn.BatchNorm2d(cout),
            nn.ReLU(inplace=True),
        )

    if arch == "wide":
        return nn.Sequential(
            block(in_ch, 64), nn.MaxPool2d(2),
            block(64, 128), nn.MaxPool2d(2),
            block(128, 256), nn.MaxPool2d(2),
            block(256, 256),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes),
        )

    return nn.Sequential(
        block(in_ch, 32), nn.MaxPool2d(2),
        block(32, 64), nn.MaxPool2d(2),
        block(64, 128), nn.MaxPool2d(2),
        nn.AdaptiveAvgPool2d(1),      # -> (B,128,1,1), input-size agnostic
        nn.Flatten(),
        nn.Dropout(0.2),
        nn.Linear(128, num_classes),
    )


def get_loaders(name: str, root: str, batch_size: int, workers: int, limit: int | None,
                source: str = "auto", erase: float = 0.0):
    cfg = DATASETS[name]
    ops = [transforms.RandomCrop(cfg["size"], padding=4)]
    if cfg["hflip"]:
        ops.append(transforms.RandomHorizontalFlip())
    ops += [transforms.ToTensor(), transforms.Normalize(cfg["mean"], cfg["std"])]
    if erase > 0:
        # large-area erasing = teach the model to survive when the background is gone,
        # which is the targeted fix for the "sky -> plane" style shortcut
        ops.append(transforms.RandomErasing(p=erase, scale=(0.08, 0.50),
                                            ratio=(0.3, 3.3), value=0))
    train_tf = transforms.Compose(ops)
    test_tf = transforms.Compose([transforms.ToTensor(),
                                  transforms.Normalize(cfg["mean"], cfg["std"])])

    if source == "auto":
        local = (Path(root) / "cifar-10-batches-py").exists()
        source = "hf" if (name == "cifar10" and not local) else "torchvision"

    if source == "hf":
        train_ds = HFImageDataset("train", train_tf)
        test_ds = HFImageDataset("test", test_tf)
    else:
        train_ds = cfg["cls"](root, train=True, download=True, transform=train_tf)
        test_ds = cfg["cls"](root, train=False, download=True, transform=test_tf)

    if limit:  # smoke test: balanced subset of `limit` training images
        per_class = max(1, limit // 10)
        targets = torch.tensor(train_ds.targets)
        idx: list[int] = []
        for c in range(10):
            idx += torch.where(targets == c)[0][:per_class].tolist()
        train_ds = Subset(train_ds, idx)

    train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                          num_workers=workers, pin_memory=True, drop_last=True)
    test_dl = DataLoader(test_ds, batch_size=256, shuffle=False,
                         num_workers=workers, pin_memory=True)
    return train_dl, test_dl


@torch.no_grad()
def mix_background(x: torch.Tensor, p: float, b: int, mode: str = "image") -> torch.Tensor:
    """Replace the outer b-pixel frame, either with another sample's frame or random colour.

    This is the targeted fix the counterfactual test pointed to: it breaks the
    background<->class correlation instead of merely adding occlusion noise, so
    "sky" can no longer be a reliable cue for "bird".

    mode="image": swap the frame with another sample's frame (natural texture, weak)
    mode="color": fill the frame with a random solid colour (this mirrors the
                  ring->green counterfactual that repaired 79% of the bird->plane errors)
    """
    if x.size(0) < 2 or p <= 0:
        return x
    n, c, h, w = x.shape
    if mode == "color":
        col = (torch.rand(n, c, 1, 1, device=x.device) * 3.0) - 1.5
        src = col.expand(-1, -1, h, w)
    else:
        src = x[torch.randperm(n, device=x.device)]
    pick = torch.rand(n, 1, 1, 1, device=x.device) < p
    ring = torch.zeros_like(x, dtype=torch.bool)
    ring[:, :, :b, :] = True
    ring[:, :, -b:, :] = True
    ring[:, :, :, :b] = True
    ring[:, :, :, -b:] = True
    return torch.where(pick & ring, src, x)


def evaluate(model: nn.Module, loader: DataLoader, device: torch.device):
    model.eval()
    loss_fn = nn.CrossEntropyLoss()
    correct = total = 0
    loss_sum = 0.0
    for x, y in loader:
        x, y = x.to(device, non_blocking=True), y.to(device, non_blocking=True)
        out = model(x)
        loss_sum += loss_fn(out, y).item() * y.numel()
        correct += (out.argmax(1) == y).sum().item()
        total += y.numel()
    return loss_sum / total, correct / total


@torch.no_grad()
def dump_feature_maps(model, loader, device, cfg, out_dir: Path):
    """Save the input batch and every filter response of the first conv layer."""
    model.eval()
    x, y = next(iter(loader))
    x = x[:6].to(device)

    feats: dict[str, torch.Tensor] = {}
    conv1 = model[0][0]
    h = conv1.register_forward_hook(lambda m, i, o: feats.__setitem__("conv1", o))
    model(x)
    h.remove()
    f = feats["conv1"]

    mean = torch.tensor(cfg["mean"], device=device).view(1, -1, 1, 1)
    std = torch.tensor(cfg["std"], device=device).view(1, -1, 1, 1)
    vis = (x * std + mean).clamp(0, 1)

    out_dir.mkdir(parents=True, exist_ok=True)
    save_image(make_grid(vis, nrow=6), out_dir / "inputs.png")
    for i in range(min(6, f.shape[0])):
        # f[i] is (C_out, H, W): treat each filter response as its own 1-channel image,
        # otherwise make_grid sees "1 image with 32 channels" and PIL rejects it.
        maps = f[i].unsqueeze(1)
        maps = (maps - maps.min()) / (maps.max() - maps.min() + 1e-8)
        label = cfg["classes"][int(y[i])]
        save_image(make_grid(maps, nrow=8, padding=2),
                   out_dir / f"conv1_img{i}_label{label}.png")
    print(f"feature maps -> {out_dir}")
    print("typically: a few filters lock onto edges, others onto flat/colour regions.")


def _pyplot():
    """Import pyplot lazily so the script still runs on a machine without matplotlib."""
    try:
        import matplotlib
        matplotlib.use("Agg")          # headless: no GUI window needed
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise SystemExit("--plot needs matplotlib: python -m pip install matplotlib") from e
    return plt


@torch.no_grad()
def plot_feature_maps(model, loader, device, cfg, out_dir: Path, n: int = 4):
    """Colour grid: the input image plus the first 8 conv1 filters, one row per image."""
    plt = _pyplot()
    model.eval()
    x, y = next(iter(loader))
    x = x[:n].to(device)

    feats: dict[str, torch.Tensor] = {}
    h = model[0][0].register_forward_hook(lambda m, i, o: feats.__setitem__("conv1", o))
    model(x)
    h.remove()
    maps = feats["conv1"].detach().cpu()          # (n, 32, H, W)

    mean = torch.tensor(cfg["mean"]).view(1, -1, 1, 1)
    std = torch.tensor(cfg["std"]).view(1, -1, 1, 1)
    inputs = (x.cpu() * std + mean).clamp(0, 1)

    fig, axes = plt.subplots(n, 9, figsize=(14, 1.7 * n))
    for i in range(n):
        img = inputs[i].permute(1, 2, 0).numpy()
        axes[i, 0].imshow(img.squeeze(), cmap=None if img.shape[2] == 3 else "gray")
        axes[i, 0].set_title(f"input: {cfg['classes'][int(y[i])]}", fontsize=8)
        axes[i, 0].set_xticks([])
        axes[i, 0].set_yticks([])
        for j in range(8):
            ax = axes[i, j + 1]
            ax.imshow(maps[i, j].numpy(), cmap="viridis")
            ax.set_title(f"filter {j}", fontsize=8)
            ax.set_xticks([])
            ax.set_yticks([])
    fig.suptitle("conv1 filter responses (viridis: dark = low, yellow = high activation)",
                 fontsize=10)
    fig.tight_layout()
    path = out_dir / "conv1_grid.png"
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print(f"colour feature-map grid -> {path}")


def plot_curves(history: dict, out_dir: Path) -> None:
    """Save loss + accuracy curves collected during training."""
    plt = _pyplot()
    ep = range(1, len(history["train_loss"]) + 1)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8))
    a1.plot(ep, history["train_loss"], "o-", label="train")
    a1.plot(ep, history["test_loss"], "s-", label="test")
    a1.set_title("loss")
    a1.set_xlabel("epoch")
    a1.set_xticks(list(ep))
    a1.legend()
    a1.grid(alpha=0.3)
    a2.plot(ep, history["test_acc"], "o-", color="tab:green")
    a2.set_title("test accuracy")
    a2.set_xlabel("epoch")
    a2.set_xticks(list(ep))
    a2.set_ylim(0, 1)
    a2.grid(alpha=0.3)
    fig.tight_layout()
    path = out_dir / "curves.png"
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print(f"training curves -> {path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(DATASETS), default="mnist")
    ap.add_argument("--data-root", default=r"C:\Users\princ\cnn_demo\data")
    ap.add_argument("--out", default=r"C:\Users\princ\cnn_demo\run")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--batch-size", type=int, default=128)
    ap.add_argument("--lr", type=float, default=2e-3)
    ap.add_argument("--workers", type=int, default=0)  # 0 is safest on Windows
    ap.add_argument("--limit", type=int, default=0, help="train on N images only (smoke test)")
    ap.add_argument("--source", choices=("auto", "torchvision", "hf"), default="auto",
                    help="where CIFAR-10 comes from (auto: torchvision if extracted, else HF)")
    ap.add_argument("--arch", choices=("small", "wide"), default="small",
                    help="small = 95k params (notes' model), wide = 4 blocks ~1.5M")
    ap.add_argument("--erase", type=float, default=0.0,
                    help="probability of large-area RandomErasing (e.g. 0.5); 0 = off")
    ap.add_argument("--bg-mix", type=float, default=0.0,
                    help="probability of swapping the border frame with another sample (0 = off)")
    ap.add_argument("--bg-border", type=int, default=6, help="frame thickness for --bg-mix")
    ap.add_argument("--bg-fill", choices=("image", "color"), default="image",
                    help="image = swap frames with another sample, color = random solid frame")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dump-maps", action="store_true")
    ap.add_argument("--plot", action="store_true",
                    help="save matplotlib figures (needs matplotlib)")
    args = ap.parse_args()

    cfg = DATASETS[args.dataset]
    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    out_dir = Path(args.out) / args.dataset
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"torch {torch.__version__} | device {device} | dataset {args.dataset} | seed {args.seed}")

    train_dl, test_dl = get_loaders(args.dataset, args.data_root, args.batch_size,
                                    args.workers, args.limit or None, args.source, args.erase)
    model = build_model(cfg["in_ch"], len(cfg["classes"]), args.arch).to(device)
    print(f"train batches {len(train_dl)} | test batches {len(test_dl)} | "
          f"arch {args.arch} | params {sum(p.numel() for p in model.parameters()):,}")

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=5e-4)
    sched = torch.optim.lr_scheduler.OneCycleLR(
        opt, max_lr=args.lr, total_steps=max(1, args.epochs * len(train_dl)))
    loss_fn = nn.CrossEntropyLoss()
    best = 0.0
    history: dict[str, list[float]] = {"train_loss": [], "test_loss": [], "test_acc": []}

    for epoch in range(1, args.epochs + 1):
        model.train()
        t0, run = time.time(), 0.0
        for step, (x, y) in enumerate(train_dl, 1):
            x, y = x.to(device, non_blocking=True), y.to(device, non_blocking=True)
            if args.bg_mix > 0:
                x = mix_background(x, args.bg_mix, args.bg_border, args.bg_fill)
            opt.zero_grad(set_to_none=True)
            loss = loss_fn(model(x), y)
            loss.backward()
            opt.step()
            sched.step()
            run += loss.item()
            if step % 50 == 0 or step == len(train_dl):
                print(f"  epoch {epoch} step {step}/{len(train_dl)} loss {run / step:.4f}")

        te_loss, te_acc = evaluate(model, test_dl, device)
        history["train_loss"].append(run / max(1, len(train_dl)))
        history["test_loss"].append(te_loss)
        history["test_acc"].append(te_acc)
        print(f"epoch {epoch}: train loss {run / max(1, len(train_dl)):.4f} | "
              f"test loss {te_loss:.4f} | test acc {te_acc:.3f} | {time.time() - t0:.0f}s")

        if te_acc > best:
            best = te_acc
            torch.save(model.state_dict(), out_dir / "best.pt")
            (out_dir / "arch.txt").write_text(f"{args.arch}\n", encoding="utf-8")
            print(f"  saved {out_dir / 'best.pt'} (acc {best:.3f})")

    print(f"best test acc {best:.3f}")

    if args.dump_maps:
        dump_feature_maps(model, test_dl, device, cfg, out_dir / "featuremaps")
    if args.plot:
        if args.dump_maps:
            plot_feature_maps(model, test_dl, device, cfg, out_dir / "featuremaps")
        plot_curves(history, out_dir)


if __name__ == "__main__":
    main()

