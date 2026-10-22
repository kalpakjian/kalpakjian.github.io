r"""
background_swap.py -- counterfactual test: is the model using the background or the object?

Five conditions, same images, no retraining:

  original       nothing changed
  ring->gray     background erased, object survives   (a background shortcut would collapse)
  ring->green    background swapped to grass
  ring->sky      background swapped to more sky
  center->gray   OBJECT erased, background survives   (a background classifier would still win)

Reading:
  * predictions barely move between original / ring->* -> the model is NOT using the surround,
    so bird->plane is an information limit at 32x32, not a fixable shortcut
  * center->gray still predicts the right class with high confidence -> pure background classifier
  * ring->green / ring->sky shifts the label distribution -> genuine background dependence

Usage:
  python background_swap.py --ckpt run_A\cifar10\best.pt --class bird --n 300
"""
import argparse
from pathlib import Path

import torch

from inspect_model import scan_predictions
from train_cnn import DATASETS, _pyplot, build_model, get_loaders

RUN_ROOT = Path(r"C:\Users\princ\cnn_demo\run")


def fill_tensor(rgb, cfg):
    """A normalised constant-colour patch, ready to paste into a normalised image."""
    m = torch.tensor(cfg["mean"], dtype=torch.float32)
    s = torch.tensor(cfg["std"], dtype=torch.float32)
    c = torch.tensor(rgb, dtype=torch.float32)
    if c.numel() == 1:
        c = c.repeat(len(cfg["mean"]))
    return (c - m) / s


def apply_ring(x, fill, b):
    """Erase the outer b-pixel frame."""
    y = x.clone()
    f = fill.view(1, -1, 1, 1)
    y[:, :, :b, :] = f
    y[:, :, -b:, :] = f
    y[:, :, :, :b] = f
    y[:, :, :, -b:] = f
    return y


def apply_center(x, fill, b):
    """Erase the central square (the object)."""
    y = x.clone()
    y[:, :, b:-b, b:-b] = fill.view(1, -1, 1, 1)
    return y


def build_conditions(cfg, border):
    gray = fill_tensor(0.5, cfg)
    grass = fill_tensor((0.28, 0.42, 0.16), cfg)
    sky = fill_tensor((0.45, 0.62, 0.88), cfg)
    return {
        "original": lambda x: x,
        "ring->gray": lambda x: apply_ring(x, gray, border),
        "ring->green": lambda x: apply_ring(x, grass, border),
        "ring->sky": lambda x: apply_ring(x, sky, border),
        "center->gray": lambda x: apply_center(x, gray, border),
    }

def plot_stats(plt, classes, conds, dist, acc, flip, focus, out_path):
    """Label distribution per condition + accuracy + flip rate."""
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12.5, 4.2))

    width = 0.26
    show = [focus[0], focus[1], "other"]
    colors = ["tab:green", "tab:red", "tab:gray"]
    for j, (name, col) in enumerate(zip(show, colors)):
        vals = []
        for c in conds:
            if name == "other":
                vals.append(1.0 - dist[c].get(focus[0], 0) - dist[c].get(focus[1], 0))
            else:
                vals.append(dist[c].get(classes.index(name), 0.0))
        a1.bar([i + (j - 1) * width for i in range(len(conds))], vals, width,
               label=f"pred {name}", color=col)
    a1.set_xticks(range(len(conds)))
    a1.set_xticklabels(conds, rotation=20, ha="right", fontsize=8)
    a1.set_ylabel("share of images")
    a1.set_title(f"What the model predicts for true '{focus[0]}' images")
    a1.legend(fontsize=8)
    a1.grid(alpha=0.3, axis="y")

    a2.bar(range(len(conds)), [acc[c] for c in conds], color="tab:blue", alpha=0.85)
    a2b = a2.twinx()
    a2b.plot(range(len(conds)), [flip[c] for c in conds], "o--", color="tab:orange")
    a2b.set_ylabel("flip rate vs original", color="tab:orange")
    a2b.set_ylim(0, 1)
    for i, c in enumerate(conds):
        a2.text(i, acc[c] + 0.02, f"{acc[c]:.0%}", ha="center", fontsize=8)
    a2.set_xticks(range(len(conds)))
    a2.set_xticklabels(conds, rotation=20, ha="right", fontsize=8)
    a2.set_ylabel("accuracy")
    a2.set_ylim(0, 1.1)
    a2.set_title("Accuracy (bars) and label flip rate (line)")
    a2.grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  stats -> {out_path}")


def plot_examples(plt, cfg, conds, imgs, labels, preds, out_path, n=3):
    """Rows = images, columns = conditions, titled with the predicted label."""
    import numpy as np

    mean = torch.tensor(cfg["mean"]).view(1, -1, 1, 1)
    std = torch.tensor(cfg["std"]).view(1, -1, 1, 1)
    names = list(conds)
    fig, axes = plt.subplots(n, len(names), figsize=(2.1 * len(names), 2.3 * n))
    for r in range(n):
        for c, cname in enumerate(names):
            img = imgs[cname][r]
            vis = (img * std[0] + mean[0]).clamp(0, 1).permute(1, 2, 0).numpy()
            ax = axes[r, c]
            ax.imshow(vis.squeeze(), cmap=None if vis.shape[2] == 3 else "gray")
            ax.set_xticks([])
            ax.set_yticks([])
            if r == 0:
                ax.set_title(cname, fontsize=9)
            if c == 0:
                ax.set_ylabel(f"true {cfg['classes'][int(labels[r])]}", fontsize=8)
            ax.set_xlabel(f"pred {cfg['classes'][int(preds[cname][r])]}", fontsize=7)
    fig.suptitle("Same image, five counterfactuals", fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  examples -> {out_path}")



def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(DATASETS), default="cifar10")
    ap.add_argument("--ckpt", default="")
    ap.add_argument("--class", dest="cls", default="bird")
    ap.add_argument("--n", type=int, default=300, help="how many images of that class")
    ap.add_argument("--border", type=int, default=6, help="frame thickness to replace")
    ap.add_argument("--show", type=int, default=3, help="example rows in the figure")
    ap.add_argument("--subset", default="all",
                    help="all | errors (misclassified) | errors:<class> (misclassified as that)")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()

    cfg = DATASETS[args.dataset]
    classes = list(cfg["classes"])
    if args.cls not in classes:
        raise SystemExit(f"unknown class {args.cls!r}; choose from {classes}")
    cidx = classes.index(args.cls)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    ckpt = Path(args.ckpt) if args.ckpt else RUN_ROOT / args.dataset / "best.pt"
    out_dir = ckpt.parent / "inspect"
    out_dir.mkdir(parents=True, exist_ok=True)
    arch_file = ckpt.parent / "arch.txt"
    arch = arch_file.read_text(encoding="utf-8").strip() if arch_file.exists() else "small"

    _, test_dl = get_loaders(args.dataset, r"C:\Users\princ\cnn_demo\data", 256, 0, None)
    model = build_model(cfg["in_ch"], len(classes), arch).to(device)
    model.load_state_dict(torch.load(ckpt, map_location=device))
    model.eval()

    imgs, labels, preds, _ = scan_predictions(model, test_dl, device)
    mask = labels == cidx
    if args.subset.startswith("errors"):
        mask = mask & (preds != labels)
        if ":" in args.subset:
            tgt = args.subset.split(":", 1)[1].strip()
            if tgt not in classes:
                raise SystemExit(f"unknown target class {tgt!r}")
            mask = mask & (preds == classes.index(tgt))
    idx = torch.where(mask)[0][: args.n]
    if len(idx) == 0:
        raise SystemExit(f"no images matched subset {args.subset!r}")
    x0 = imgs[idx].to(device)
    print(f"loaded {ckpt} | arch {arch} | class '{args.cls}' | subset {args.subset} "
          f"| n={len(idx)} | border={args.border}")

    conds = build_conditions(cfg, args.border)
    dist, acc, flip, pred_by_cond, imgs_by_cond = {}, {}, {}, {}, {}
    base_pred = None
    for name, fn in conds.items():
        xb = fn(x0)
        with torch.no_grad():
            probs = model(xb).softmax(1)
        p = probs.argmax(1)
        if base_pred is None:
            base_pred = p
        counts = torch.bincount(p, minlength=len(classes)).float() / len(p)
        dist[name] = {i: float(v) for i, v in enumerate(counts)}
        acc[name] = float((p == cidx).float().mean())
        flip[name] = float((p != base_pred).float().mean())
        pred_by_cond[name] = p.cpu()
        imgs_by_cond[name] = xb.cpu()

    # top confusions for the original and for the object-erased condition
    focus = [args.cls]
    others = [classes[j] for j in torch.argsort(torch.tensor([dist["original"][k] for k in range(len(classes))]),
                                                descending=True).tolist() if j != cidx][:2]
    focus += others

    plt = _pyplot()
    tag = f"_{args.tag}" if args.tag else ""
    plot_stats(plt, classes, list(conds), dist, acc, flip, focus, out_dir / f"swap_stats{tag}.png")
    kept = {k: imgs_by_cond[k][: args.show] for k in conds}
    plot_examples(plt, cfg, conds, kept, labels[idx][: args.show], 
                  {k: pred_by_cond[k][: args.show] for k in conds},
                  out_dir / f"swap_examples{tag}.png", n=min(args.show, len(idx)))

    rep = [f"ckpt={ckpt} arch={arch} class={args.cls} n={len(idx)} border={args.border}", ""]
    for name in conds:
        top = sorted(dist[name].items(), key=lambda kv: -kv[1])[:3]
        tops = ", ".join(f"{classes[k]}={v * 100:.1f}%" for k, v in top)
        rep.append(f"{name:13} acc={acc[name] * 100:5.1f}% flip={flip[name] * 100:5.1f}% | top: {tops}")
    rep += ["",
            f"P({args.cls}) original={dist['original'][cidx] * 100:.1f}% "
            f"ring->gray={dist['ring->gray'][cidx] * 100:.1f}% "
            f"center->gray={dist['center->gray'][cidx] * 100:.1f}%",
            "reading: if ring->* barely changes anything the model is not using the surround;",
            "         if center->gray keeps the accuracy the model is a background classifier."]
    (out_dir / f"swap{tag}.txt").write_text("\n".join(rep) + "\n", encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
