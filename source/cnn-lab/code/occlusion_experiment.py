r"""
occlusion_experiment.py -- is a low occlusion ratio a *property of the mistakes*?

Hypothesis (from the earlier single-image analysis): the model's confident errors are
not supported by any local region (ratio = max_drop / margin ~ 0.1), while correct
predictions are. If that holds statistically, the low ratio is a signature of the
shortcut, not a quirk of one unlucky image.

Two measurements per sample:
  1. ratio   = max occlusion drop / (top1 - top2 margin)
  2. spread  = mean drop inside the centre box  vs  the border ring
               (a model leaning on background should lose more from the border)

Outputs (run\<dataset>\inspect\):
  ratio_compare.png   strip plot of ratios by group + centre/border bars
  ratio_examples.png  k correct vs k wrong, with the occlusion map
  ratio_compare.txt   per-sample numbers and summary statistics

Usage:
  python occlusion_experiment.py --dataset cifar10 --class bird --k 12
  python occlusion_experiment.py --dataset mnist   --class 7    --k 12
"""
import argparse
import random
from pathlib import Path

import torch

from inspect_model import occlusion_sensitivity, scan_predictions
from train_cnn import DATASETS, _pyplot, build_model, get_loaders

RUN_ROOT = Path(r"C:\Users\princ\cnn_demo\run")


def centre_border_drop(drop, size, margin_frac=0.25):
    """Mean confidence drop inside the centre box vs the outer ring.

    `margin_frac` is the fraction of the image skipped on each side to form the centre.
    """
    n, h, w = drop.shape
    m = int(round(min(h, w) * margin_frac))
    centre = drop[:, m:h - m, m:w - m].mean(dim=(1, 2))
    mask = torch.ones(h, w, dtype=torch.bool, device=drop.device)
    mask[m:h - m, m:w - m] = False
    border = drop[:, mask].mean(dim=1)
    return centre, border


def pick_group(labels, preds, confs, class_idx, k, want_correct, seed=0,
               min_conf=0.0, max_conf=1.01):
    """Random sample of (in)correct predictions for one class, optionally in a confidence band."""
    hit = ((labels == class_idx) & ((preds == labels) == want_correct)
           & (confs >= min_conf) & (confs <= max_conf))
    idx = torch.where(hit)[0]
    if len(idx) == 0:
        return idx
    rng = random.Random(seed)
    chosen = rng.sample(idx.tolist(), min(k, len(idx)))
    return torch.tensor(sorted(chosen))


def plot_stats(plt, groups, out_path, threshold=0.15):
    """Strip plot of ratios per group + centre/border evidence split."""
    names = list(groups)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))

    for j, name in enumerate(names):
        vals = groups[name]["ratio"]
        xs = [j + (random.Random(i).random() - 0.5) * 0.22 for i in range(len(vals))]
        a1.scatter(xs, vals, s=34, alpha=0.85, label=name)
        a1.hlines(sum(vals) / len(vals), j - 0.22, j + 0.22, color="black", lw=2)
        a1.annotate(f"mean {sum(vals) / len(vals):.2f}", (j, sum(vals) / len(vals)),
                    textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)
    a1.axhline(threshold, color="crimson", ls="--", lw=1.2)
    a1.text(len(names) - 0.5, threshold, " 0.15 = 'no decisive region'", color="crimson",
            fontsize=8, va="bottom", ha="right")
    a1.set_xticks(range(len(names)))
    a1.set_xticklabels(names)
    a1.set_ylabel("ratio = max_drop / margin")
    a1.set_title("Local evidence per sample")
    a1.grid(alpha=0.3, axis="y")
    a1.legend(fontsize=8)

    width = 0.36
    for j, name in enumerate(names):
        a2.bar(j - width / 2, groups[name]["centre"], width, label="centre" if j == 0 else None)
        a2.bar(j + width / 2, groups[name]["border"], width, label="border" if j == 0 else None)
    a2.set_xticks(range(len(names)))
    a2.set_xticklabels(names)
    a2.set_ylabel("mean confidence drop")
    a2.set_title("Where the evidence sits (centre vs border)")
    a2.grid(alpha=0.3, axis="y")
    a2.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  stats -> {out_path}")


def plot_examples(plt, cfg, imgs, labels, preds, drop, ratio, groups, out_path):
    """k correct vs k wrong, each with its occlusion map."""
    import numpy as np

    mean = torch.tensor(cfg["mean"]).view(1, -1, 1, 1)
    std = torch.tensor(cfg["std"]).view(1, -1, 1, 1)
    vis = (imgs * std + mean).clamp(0, 1)

    rows = []
    for name in groups:
        for i in groups[name]["order"]:
            rows.append((name, i))
    n = len(rows)
    fig, axes = plt.subplots(n, 3, figsize=(6.4, 1.75 * n))
    for r, (name, i) in enumerate(rows):
        img = vis[i].permute(1, 2, 0).numpy().squeeze()
        base = img if img.ndim == 3 else np.stack([img] * 3, -1)
        d = drop[i].numpy()
        vmax = max(abs(d).max(), 1e-6)
        blended = (0.55 * base + 0.45 * plt.cm.bwr(d / (2 * vmax) + 0.5)[..., :3]).clip(0, 1)
        axes[r, 0].imshow(img, cmap=None if img.ndim == 3 else "gray")
        axes[r, 0].set_title(f"{name} | true {cfg['classes'][int(labels[i])]}", fontsize=8)
        axes[r, 1].imshow(d, cmap="bwr", vmin=-vmax, vmax=vmax)
        axes[r, 1].set_title(f"drop (max {d.max():.2f})", fontsize=8)
        axes[r, 2].imshow(blended)
        axes[r, 2].set_title(f"pred {cfg['classes'][int(preds[i])]} | ratio {ratio[i]:.2f}",
                             fontsize=8)
        for ax in axes[r]:
            ax.set_xticks([])
            ax.set_yticks([])
    fig.suptitle("Occlusion: correct vs misclassified, same class", fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  examples -> {out_path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(DATASETS), default="cifar10")
    ap.add_argument("--class", dest="cls", default="bird",
                    help="class name (cifar10) or digit (mnist)")
    ap.add_argument("--k", type=int, default=12, help="samples per group")
    ap.add_argument("--patch", type=int, default=8)
    ap.add_argument("--stride", type=int, default=4)
    ap.add_argument("--ckpt", default="")
    ap.add_argument("--min-conf", type=float, default=0.0,
                    help="only sample predictions with confidence >= this (controls the margin)")
    ap.add_argument("--max-conf", type=float, default=1.01,
                    help="only sample predictions with confidence <= this")
    ap.add_argument("--tag", default="", help="suffix for the output filenames")
    args = ap.parse_args()

    cfg = DATASETS[args.dataset]
    if args.cls not in cfg["classes"]:
        raise SystemExit(f"unknown class {args.cls!r}; choose from {cfg['classes']}")
    class_idx = cfg["classes"].index(args.cls)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    run_dir = RUN_ROOT / args.dataset
    ckpt = Path(args.ckpt) if args.ckpt else run_dir / "best.pt"
    out_dir = ckpt.parent / "inspect"
    arch_file = ckpt.parent / "arch.txt"
    arch = arch_file.read_text(encoding="utf-8").strip() if arch_file.exists() else "small"
    out_dir.mkdir(parents=True, exist_ok=True)

    _, test_dl = get_loaders(args.dataset, r"C:\Users\princ\cnn_demo\data", 256, 0, None)
    model = build_model(cfg["in_ch"], len(cfg["classes"]), arch).to(device)
    model.load_state_dict(torch.load(ckpt, map_location=device))
    model.eval()
    print(f"loaded {ckpt} | arch {arch} | {device} | class={args.cls} | k={args.k}")

    imgs, labels, preds, confs = scan_predictions(model, test_dl, device)
    n_cls = int((labels == class_idx).sum())
    n_wrong = int(((labels == class_idx) & (preds != labels)).sum())
    acc_cls = 1 - n_wrong / max(n_cls, 1)
    print(f"class {args.cls}: {n_cls} test images, {n_wrong} misclassified "
          f"(accuracy {acc_cls:.1%})")

    order_correct = pick_group(labels, preds, confs, class_idx, args.k, True,
                               min_conf=args.min_conf, max_conf=args.max_conf)
    order_wrong = pick_group(labels, preds, confs, class_idx, args.k, False,
                             min_conf=args.min_conf, max_conf=args.max_conf)
    if len(order_wrong) == 0:
        raise SystemExit(f"no misclassified samples in the confidence band "
                         f"[{args.min_conf}, {args.max_conf}] - try a wider band")
    print(f"  correct sample: {len(order_correct)} | wrong sample: {len(order_wrong)}")

    sel = torch.cat([order_correct, order_wrong])
    x = imgs[sel].to(device)
    drop, base_prob, oc_pred, margin = occlusion_sensitivity(model, x, args.patch, args.stride)
    ratio = (drop.amax(dim=(1, 2)) / margin.clamp(min=1e-6)).cpu()
    centre, border = centre_border_drop(drop.cpu(), x.shape[-1])

    kc = len(order_correct)
    groups = {
        "correct": {"order": list(range(kc)),
                    "ratio": ratio[:kc].tolist(),
                    "centre": float(centre[:kc].mean()),
                    "border": float(border[:kc].mean())},
        "misclassified": {"order": list(range(kc, len(sel))),
                          "ratio": ratio[kc:].tolist(),
                          "centre": float(centre[kc:].mean()),
                          "border": float(border[kc:].mean())},
    }

    plt = _pyplot()
    tag = f"_{args.tag}" if args.tag else ""
    plot_stats(plt, groups, out_dir / f"ratio_compare{tag}.png")
    plot_examples(plt, cfg, imgs[sel], labels[sel], oc_pred.cpu(), drop.cpu(), ratio,
                  groups, out_dir / f"ratio_examples{tag}.png")

    rep = [f"dataset={args.dataset} class={args.cls} "
           f"({n_cls} images, {n_wrong} wrong, acc {acc_cls:.1%})",
           f"patch={args.patch} stride={args.stride} "
           f"confidence band=[{args.min_conf}, {args.max_conf}]", ""]
    for name, g in groups.items():
        r = g["ratio"]
        rep.append(f"{name:14} n={len(r):2d} mean_ratio={sum(r) / len(r):.3f} "
                   f"median={sorted(r)[len(r) // 2]:.3f} max={max(r):.3f} min={min(r):.3f} "
                   f"| centre_drop={g['centre']:.3f} border_drop={g['border']:.3f} "
                   f"ratio_of_drops={g['centre'] / max(g['border'], 1e-6):.2f}")
        for i in g["order"]:
            idx = int(sel[i])
            rep.append(f"    true={cfg['classes'][int(labels[idx])]:5} "
                       f"pred={cfg['classes'][int(oc_pred[i])]:5} "
                       f"p={base_prob[i]:.3f} ratio={ratio[i]:.3f} "
                       f"centre={centre[i]:.3f} border={border[i]:.3f}")
    rep += ["", "reading: centre/border > 1 means the model's evidence sits on the object,"
                " < 1 means it leans on the frame/background"]
    (out_dir / f"ratio_compare{tag}.txt").write_text("\n".join(rep) + "\n", encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
