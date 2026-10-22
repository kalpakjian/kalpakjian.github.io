r"""
inspect_model.py -- look inside a trained CNN: conv2/conv3 feature maps + Grad-CAM.

Loads the weights saved by train_cnn.py (run\<dataset>\best.pt) and writes:

  inspect\conv1_grid.png   top-8 channels of block 1  (28x28 on MNIST)
  inspect\conv2_grid.png   top-8 channels of block 2  (14x14)
  inspect\conv3_grid.png   top-8 channels of block 3  (7x7)
  inspect\gradcam.png      input | Grad-CAM heatmap | overlay, per image
  inspect\summary.txt      top-5 predictions + confidence per image

Why the grids shrink: 28 -> pool 14 -> conv2 14x14 -> pool 7 -> conv3 7x7.
Deeper layers trade spatial resolution for channels (32 -> 64 -> 128), which is
exactly the "low-level detail -> high-level concept" trade of a CNN.

Usage:
  python inspect_model.py --dataset mnist
  python inspect_model.py --dataset mnist --ckpt run\\mnist\\best.pt --n 4
"""
import argparse
from pathlib import Path

import torch
import torch.nn.functional as F

from train_cnn import DATASETS, _pyplot, build_model, get_loaders

# model is nn.Sequential: 0=block1 1=pool 2=block2 3=pool 4=block3 5=GAP 6=flatten 7=drop 8=fc
LAYER_INDEX = {"conv1": 0, "conv2": 2, "conv3": 4}


def conv_of(model: torch.nn.Module, name: str) -> torch.nn.Module:
    """Return the Conv2d inside the given residual-free block."""
    return model[LAYER_INDEX[name]][0]


@torch.no_grad()
def grab_features(model, x, names):
    """Capture the output of several conv layers in one forward pass."""
    feats: dict[str, torch.Tensor] = {}
    handles = [
        conv_of(model, n).register_forward_hook(
            lambda m, i, o, k=n: feats.__setitem__(k, o.detach().cpu()))
        for n in names
    ]
    model(x)
    for h in handles:
        h.remove()
    return feats


def plot_layer_grid(plt, feats, inputs, labels, layer, out_path, n_img=4, n_ch=8):
    """One row per image, one column per (most active) channel of that layer."""
    f = feats[layer]                                  # (N, C, H, W)
    n_img = min(n_img, f.shape[0])                    # respect --n
    order = f.mean(dim=(0, 2, 3)).argsort(descending=True)[:n_ch].tolist()
    h, w = f.shape[-2:]

    fig, axes = plt.subplots(n_img, n_ch + 1, figsize=(1.45 * (n_ch + 1), 1.75 * n_img))
    for i in range(n_img):
        img = inputs[i].permute(1, 2, 0).numpy()
        axes[i, 0].imshow(img.squeeze(), cmap=None if img.shape[2] == 3 else "gray")
        axes[i, 0].set_title(f"input: {labels[i]}", fontsize=8)
        axes[i, 0].set_xticks([])
        axes[i, 0].set_yticks([])
        for j, c in enumerate(order):
            ax = axes[i, j + 1]
            ax.imshow(f[i, c].numpy(), cmap="viridis")
            ax.set_title(f"ch{c}", fontsize=7)
            ax.set_xticks([])
            ax.set_yticks([])
    fig.suptitle(f"{layer} feature maps  ({f.shape[1]} channels, {h}x{w}) "
                 f"- showing the 8 most active", fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  {layer}: {f.shape[1]}ch {h}x{w} -> {out_path}")


def grad_cam(model, x, layer: str = "conv3"):
    """Grad-CAM: weight each channel by the gradient of the predicted class.

    Returns (cam (N,H,W) in 0..1, pred, logits). Standard recipe:
      w_c = mean over space of d(score)/d(A_c)   -> importance per channel
      CAM = ReLU(sum_c w_c * A_c)                -> only positive evidence
    """
    conv = conv_of(model, layer)
    feats: dict[str, torch.Tensor] = {}
    grads: dict[str, torch.Tensor] = {}
    h1 = conv.register_forward_hook(lambda m, i, o: feats.__setitem__("a", o))
    h2 = conv.register_full_backward_hook(lambda m, gi, go: grads.__setitem__("g", go[0]))

    model.zero_grad(set_to_none=True)
    logits = model(x)
    pred = logits.argmax(1)
    rows = torch.arange(len(x), device=x.device)
    logits[rows, pred].sum().backward()          # score = sum of predicted-class logits
    h1.remove()
    h2.remove()

    a = feats["a"].detach()                      # (N, C, h, w)
    g = grads["g"].detach()
    weights = g.mean(dim=(2, 3), keepdim=True)   # (N, C, 1, 1)
    cam = F.relu((weights * a).sum(1, keepdim=True))
    cam = F.interpolate(cam, size=x.shape[-2:], mode="bilinear", align_corners=False)
    cam = cam.squeeze(1)
    lo = cam.amin(dim=(1, 2), keepdim=True)
    hi = cam.amax(dim=(1, 2), keepdim=True)
    cam = (cam - lo) / (hi - lo + 1e-8)
    return cam.detach().cpu(), pred.detach().cpu(), logits.detach().cpu()


def plot_gradcam(plt, cam, inputs, labels, preds, probs, cfg, out_path, layer="conv3"):
    """input | heatmap | overlay, one row per image."""
    import numpy as np

    n = len(inputs)
    fig, axes = plt.subplots(n, 3, figsize=(7.5, 2.1 * n))
    for i in range(n):
        img = inputs[i].permute(1, 2, 0).numpy()
        img = img.squeeze()
        heat = cam[i].numpy()
        overlay = img if img.ndim == 3 else np.stack([img] * 3, -1)
        rgba = plt.cm.jet(heat)
        blended = (0.55 * overlay + 0.45 * rgba[..., :3]).clip(0, 1)

        axes[i, 0].imshow(img, cmap=None if img.ndim == 3 else "gray")
        axes[i, 0].set_title(f"input: {labels[i]}", fontsize=9)
        axes[i, 1].imshow(heat, cmap="jet")
        axes[i, 1].set_title(f"Grad-CAM ({layer})", fontsize=9)
        axes[i, 2].imshow(blended)
        axes[i, 2].set_title(f"pred: {preds[i]} ({probs[i]:.1%})", fontsize=9)
        for ax in axes[i]:
            ax.set_xticks([])
            ax.set_yticks([])
    fig.suptitle(f"Grad-CAM on {layer}: where the model looked (red = decisive evidence)",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  Grad-CAM ({layer}) -> {out_path}")


@torch.no_grad()
def scan_predictions(model, loader, device):
    """One pass over the test set: collect inputs, labels, predictions, confidence."""
    model.eval()
    imgs, labels, preds, confs = [], [], [], []
    for x, y in loader:
        x = x.to(device)
        p = model(x).softmax(1)
        conf, pr = p.max(1)
        imgs.append(x.cpu())
        labels.append(y)
        preds.append(pr.cpu())
        confs.append(conf.cpu())
    return torch.cat(imgs), torch.cat(labels), torch.cat(preds), torch.cat(confs)


def pick_samples(labels, preds, confs, k=3):
    """k most confident mistakes  +  k least confident correct predictions."""
    wrong = preds != labels
    idx_wrong = torch.where(wrong)[0][confs[wrong].argsort(descending=True)][:k]
    idx_unsure = torch.where(~wrong)[0][confs[~wrong].argsort()][:k]
    return idx_wrong, idx_unsure


def plot_errors(plt, model, cfg, imgs, labels, preds, confs, idx_wrong, idx_unsure,
                out_path, layer="conv2"):
    """input | Grad-CAM | overlay for the worst cases (misclassified + unsure)."""
    import numpy as np

    device = next(model.parameters()).device
    idx = torch.cat([idx_wrong, idx_unsure])
    if len(idx) == 0:
        print("  no errors to show")
        return
    cam, _, _ = grad_cam(model, imgs[idx].to(device), layer)
    cam = cam.cpu()

    mean = torch.tensor(cfg["mean"]).view(1, -1, 1, 1)
    std = torch.tensor(cfg["std"]).view(1, -1, 1, 1)
    vis = (imgs[idx] * std + mean).clamp(0, 1)

    n = len(idx)
    fig, axes = plt.subplots(n, 3, figsize=(7.6, 1.95 * n))
    for r in range(n):
        i = int(idx[r])
        tag = "MISCLASSIFIED" if r < len(idx_wrong) else "LOW CONFIDENCE"
        img = vis[r].permute(1, 2, 0).numpy().squeeze()
        base = img if img.ndim == 3 else np.stack([img] * 3, -1)
        blended = (0.55 * base + 0.45 * plt.cm.jet(cam[r].numpy())[..., :3]).clip(0, 1)
        axes[r, 0].imshow(img, cmap=None if img.ndim == 3 else "gray")
        axes[r, 0].set_title(f"{tag} | true {cfg['classes'][int(labels[i])]}", fontsize=8)
        axes[r, 1].imshow(cam[r].numpy(), cmap="jet")
        axes[r, 1].set_title(f"Grad-CAM ({layer})", fontsize=8)
        axes[r, 2].imshow(blended)
        axes[r, 2].set_title(f"pred {cfg['classes'][int(preds[i])]} p={confs[i]:.1%}", fontsize=8)
        for ax in axes[r]:
            ax.set_xticks([])
            ax.set_yticks([])
    fig.suptitle("Failure analysis: where the model looked when it went wrong", fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  error analysis -> {out_path}")


def plot_kernels(plt, model, out_path, n=32):
    """Visualise the conv1 weights themselves (not their responses)."""
    import numpy as np

    w = model[0][0].weight.detach().cpu()      # (C_out, C_in, 3, 3)
    w = w.mean(1)                              # average over input channels for display
    vmax = max(w.abs().max().item(), 1e-8)
    cols = 8
    rows = (min(n, w.shape[0]) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(1.9 * cols, 2.0 * rows))
    for i in range(rows * cols):
        ax = axes[i // cols][i % cols]
        ax.axis("off")
        if i >= min(n, w.shape[0]):
            continue
        k = w[i].numpy()
        ax.imshow(k, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
        ax.set_title(f"k{i}  |w|={np.linalg.norm(k):.2f}", fontsize=7)
        for (r, c), val in np.ndenumerate(k):
            ax.text(c, r, f"{val:+.2f}", ha="center", va="center", fontsize=6,
                    color="white" if abs(val) > 0.6 * vmax else "black")
    fig.suptitle("conv1 kernels (3x3, red = positive weight, blue = negative) - "
                 "what the filters are tuned for", fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  kernels -> {out_path}")


@torch.no_grad()
def occlusion_sensitivity(model, x, patch=8, stride=4, fill=0.0):
    """Slide an occluding square over the image and record the confidence drop.

    For every window position we erase that patch, rerun the model and record
    prob(predicted class). Interpretation:
      * large drop  -> the model NEEDED that region (real evidence)
      * rise (blue) -> that region was evidence AGAINST the prediction
      * everywhere flat -> the model is not using local evidence at all
        (this is the quantitative proof of a background/shortcut dependence
        that Grad-CAM can only hint at by showing an empty heatmap)

    Returns (drop (N,H,W), base_prob (N,), pred (N,), margin (N,)).
    """
    model.eval()
    n, _, h, w = x.shape
    probs = model(x).softmax(1)
    top2 = probs.topk(2, dim=1).values
    base_prob, pred = probs.max(1)
    margin = top2[:, 0] - top2[:, 1]           # how sure the model is relative to runner-up
    rows = torch.arange(n, device=x.device)
    acc = torch.zeros(n, h, w, device=x.device)
    cnt = torch.zeros(h, w, device=x.device)
    for y in range(0, h - patch + 1, stride):
        for xx in range(0, w - patch + 1, stride):
            occluded = x.clone()
            occluded[:, :, y:y + patch, xx:xx + patch] = fill
            p = model(occluded).softmax(1)[rows, pred]
            acc[:, y:y + patch, xx:xx + patch] += p[:, None, None]
            cnt[y:y + patch, xx:xx + patch] += 1
    occ_prob = acc / cnt.clamp(min=1)[None]
    return base_prob[:, None, None] - occ_prob, base_prob, pred, margin


def plot_occlusion(plt, cfg, imgs, labels, preds, base_prob, drop, out_path, patch, stride,
                   ratio=None):
    """input | confidence drop | overlay, plus max-drop / margin ratio per image."""
    import numpy as np

    mean = torch.tensor(cfg["mean"]).view(1, -1, 1, 1)
    std = torch.tensor(cfg["std"]).view(1, -1, 1, 1)
    vis = (imgs * std + mean).clamp(0, 1)

    n = len(imgs)
    fig, axes = plt.subplots(n, 3, figsize=(7.8, 2.05 * n))
    for i in range(n):
        img = vis[i].permute(1, 2, 0).numpy().squeeze()
        base = img if img.ndim == 3 else np.stack([img] * 3, -1)
        d = drop[i].cpu().numpy()
        vmax = max(abs(d).max(), 1e-6)
        blended = (0.55 * base + 0.45 * plt.cm.bwr(d / (2 * vmax) + 0.5)[..., :3]).clip(0, 1)

        axes[i, 0].imshow(img, cmap=None if img.ndim == 3 else "gray")
        axes[i, 0].set_title(f"true {labels[i]}", fontsize=9)
        im = axes[i, 1].imshow(d, cmap="bwr", vmin=-vmax, vmax=vmax)
        axes[i, 1].set_title("confidence drop", fontsize=9)
        axes[i, 2].imshow(blended)
        r = f" | r={ratio[i]:.2f}" if ratio is not None else ""
        axes[i, 2].set_title(f"pred {preds[i]} {base_prob[i]:.1%} | max drop {d.max():.2f}{r}",
                             fontsize=9)
        for ax in axes[i]:
            ax.set_xticks([])
            ax.set_yticks([])
    fig.colorbar(im, ax=axes.ravel().tolist(), fraction=0.02, pad=0.01)
    fig.suptitle(f"Occlusion {patch}x{patch} stride {stride}: red = removing this hurts, "
                 f"blue = removing this helps", fontsize=10)
    fig.savefig(out_path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print(f"  occlusion -> {out_path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(DATASETS), default="mnist")
    ap.add_argument("--ckpt", default="", help="default: run\\<dataset>\\best.pt")
    ap.add_argument("--out", default="", help="default: run\\<dataset>\\inspect")
    ap.add_argument("--data-root", default=r"C:\Users\princ\cnn_demo\data")
    ap.add_argument("--n", type=int, default=4, help="how many test images to inspect")
    ap.add_argument("--errors", type=int, default=0,
                    help="also analyse this many worst cases (misclassified + unsure)")
    ap.add_argument("--kernels", action="store_true", help="also plot the conv1 kernels")
    ap.add_argument("--occlusion", action="store_true",
                    help="also run occlusion sensitivity (needs --errors for the best examples)")
    ap.add_argument("--patch", type=int, default=8, help="occlusion window size")
    ap.add_argument("--stride", type=int, default=4, help="occlusion stride")
    args = ap.parse_args()

    cfg = DATASETS[args.dataset]
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    run_dir = Path(r"C:\Users\princ\cnn_demo\run") / args.dataset
    ckpt = Path(args.ckpt) if args.ckpt else run_dir / "best.pt"
    out_dir = Path(args.out) if args.out else ckpt.parent / "inspect"
    arch_file = ckpt.parent / "arch.txt"
    arch = arch_file.read_text(encoding="utf-8").strip() if arch_file.exists() else "small"
    out_dir.mkdir(parents=True, exist_ok=True)
    if not ckpt.exists():
        raise SystemExit(f"checkpoint not found: {ckpt} -> run train_cnn.py first")

    _, test_dl = get_loaders(args.dataset, args.data_root, 8, 0, None)
    model = build_model(cfg["in_ch"], len(cfg["classes"]), arch).to(device)
    model.load_state_dict(torch.load(ckpt, map_location=device))
    model.eval()
    print(f"loaded {ckpt} | arch {arch} | device {device} | dataset {args.dataset}")

    x, y = next(iter(test_dl))
    x = x[: args.n].to(device)
    labels = [cfg["classes"][int(t)] for t in y[: args.n]]
    mean = torch.tensor(cfg["mean"]).view(1, -1, 1, 1)
    std = torch.tensor(cfg["std"]).view(1, -1, 1, 1)
    inputs = (x.cpu() * std + mean).clamp(0, 1)          # de-normalise for display

    plt = _pyplot()
    feats = grab_features(model, x, ["conv1", "conv2", "conv3"])
    for layer in ("conv1", "conv2", "conv3"):
        plot_layer_grid(plt, feats, inputs, labels, layer, out_dir / f"{layer}_grid.png")

    probs = None
    for cam_layer in ("conv2", "conv3"):
        cam, pred, logits = grad_cam(model, x, cam_layer)
        probs = logits.softmax(1)
        rows = torch.arange(len(x))
        conf = probs[rows, pred]
        plot_gradcam(plt, cam, inputs, labels,
                     [cfg["classes"][int(p)] for p in pred], conf.tolist(),
                     cfg, out_dir / f"gradcam_{cam_layer}.png", layer=cam_layer)

    lines = []
    for i in range(len(x)):
        top5 = probs[i].topk(5)
        ranked = ", ".join(f"{cfg['classes'][int(k)]}:{v:.3f}"
                           for v, k in zip(top5.values, top5.indices))
        lines.append(f"img{i}  true={labels[i]}  pred={cfg['classes'][int(pred[i])]}  "
                     f"p={conf[i]:.3f}  | top5: {ranked}")
    (out_dir / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))

    if args.kernels:
        plot_kernels(plt, model, out_dir / "kernels_conv1.png")

    if args.errors > 0:
        print("scanning the test set for failures...")
        all_imgs, all_lab, all_pred, all_conf = scan_predictions(model, test_dl, device)
        iw, iu = pick_samples(all_lab, all_pred, all_conf, k=args.errors)
        plot_errors(plt, model, cfg, all_imgs, all_lab, all_pred, all_conf, iw, iu,
                    out_dir / "errors.png", layer="conv2")

        acc = (all_pred == all_lab).float().mean().item()
        rep = [f"test accuracy: {acc:.4f}  "
               f"({int((all_pred == all_lab).sum())}/{len(all_lab)})", ""]
        for tag, ids in (("MISCLASSIFIED", iw), ("LOW-CONFIDENCE CORRECT", iu)):
            for i in ids:
                rep.append(f"{tag}: true={cfg['classes'][int(all_lab[i])]} "
                           f"pred={cfg['classes'][int(all_pred[i])]} p={all_conf[i]:.3f}")
        (out_dir / "errors.txt").write_text("\n".join(rep) + "\n", encoding="utf-8")
        print("\n".join(rep))

    if args.occlusion:
        if args.errors > 0 and len(iw) > 0:
            occ_imgs = all_imgs[iw]              # the misclassified ones are the instructive ones
            occ_lab = all_lab[iw]
        else:
            occ_imgs = x.cpu()
            occ_lab = y[: args.n]
        drop, base_prob, oc_pred, margin = occlusion_sensitivity(
            model, occ_imgs.to(device), args.patch, args.stride)
        ratio = (drop.amax(dim=(1, 2)) / margin.clamp(min=1e-6)).tolist()
        plot_occlusion(plt, cfg, occ_imgs,
                       [cfg["classes"][int(t)] for t in occ_lab],
                       [cfg["classes"][int(p)] for p in oc_pred],
                       base_prob.tolist(), drop.cpu(), out_dir / "occlusion.png",
                       args.patch, args.stride, ratio)

        occ_rep = []
        w_img = drop.shape[-1]
        for i in range(len(occ_imgs)):
            d = drop[i]
            flat = int(torch.argmax(d))
            r = ratio[i]
            if r >= 0.5:
                verdict = "STRONG local evidence"
            elif r >= 0.15:
                verdict = "partial / distributed evidence"
            else:
                verdict = "NO single decisive region -> global cue or shortcut"
            occ_rep.append(
                f"img{i} true={cfg['classes'][int(occ_lab[i])]} "
                f"pred={cfg['classes'][int(oc_pred[i])]} base={base_prob[i]:.3f} "
                f"margin={margin[i]:.3f} max_drop={d.max():.3f} at (y={flat // w_img}, x={flat % w_img}) "
                f"ratio={r:.2f} mean_drop={d.mean():.3f} -> {verdict}")
        (out_dir / "occlusion.txt").write_text("\n".join(occ_rep) + "\n", encoding="utf-8")
        print("\n".join(occ_rep))

    print(f"done -> {out_dir}")


if __name__ == "__main__":
    main()
