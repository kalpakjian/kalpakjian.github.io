r"""
error_taxonomy.py -- split the model's mistakes by "how decisive the local evidence was",
then look at the Grad-CAM of the decisively-wrong ones.

Phase 1 (taxonomy): for several classes, sample k confident-correct and k confident-wrong
images, run occlusion on all of them and classify each mistake as
    decisive  ratio >= --decisive   a local cue drove the (wrong) answer -> explainable
    blind     ratio <  --blind      no decisive cue at all               -> hard / ambiguous
    mixed     in between
Phase 2 (look): for up to --show decisive mistakes, save input | Grad-CAM | occlusion so you
can check whether they all latch onto the same kind of part (sky, grass, a wheel, ...).

Outputs go to <ckpt dir>\inspect\:
    taxonomy.png / taxonomy.txt / decisive_wrong.png

Usage:
  python error_taxonomy.py --dataset cifar10 --classes bird,dog,ship --k 40
  python error_taxonomy.py --dataset cifar10 --classes bird --k 40 --ckpt run_wide\cifar10\best.pt
"""
import argparse
from pathlib import Path

import torch

from inspect_model import grad_cam, occlusion_sensitivity, scan_predictions
from occlusion_experiment import centre_border_drop, pick_group
from train_cnn import DATASETS, _pyplot, build_model, get_loaders

RUN_ROOT = Path(r"C:\Users\princ\cnn_demo\run")


def classify(ratio, decisive, blind):
    """Three-way label for one sample's ratio."""
    if ratio >= decisive:
        return "decisive"
    if ratio < blind:
        return "blind"
    return "mixed"


def plot_taxonomy(plt, classes, stats, pooled, decisive, blind, out_path):
    """Per-class mean ratio, error-type composition, and the pooled strip plot."""
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(14.5, 4.3), width_ratios=[1.1, 1.0, 1.0])

    # (a) per-class mean ratio: correct vs wrong
    width = 0.36
    for j, cname in enumerate(classes):
        s = stats[cname]
        a1.bar(j - width / 2, s["correct_mean"], width, color="tab:blue")
        a1.bar(j + width / 2, s["wrong_mean"], width, color="tab:orange")
        a1.annotate(f"{s['wrong_mean']:.2f}", (j + width / 2, s["wrong_mean"]),
                    textcoords="offset points", xytext=(0, 4), ha="center", fontsize=8)
    a1.set_xticks(range(len(classes)))
    a1.set_xticklabels(classes)
    a1.set_ylabel("mean ratio")
    a1.set_title("Mean ratio: correct (blue) vs wrong (orange)")
    a1.grid(alpha=0.3, axis="y")

    # (b) composition of the mistakes
    labels = ["decisive", "mixed", "blind"]
    colors = {"decisive": "tab:red", "mixed": "tab:gray", "blind": "tab:blue"}
    bottoms = [0] * len(classes)
    for kind in labels:
        vals = [stats[c]["kinds"].get(kind, 0) / max(stats[c]["n_wrong"], 1) for c in classes]
        a2.bar(range(len(classes)), vals, bottom=bottoms, label=kind, color=colors[kind])
        for j, v in enumerate(vals):
            if v > 0.06:
                a2.text(j, bottoms[j] + v / 2, f"{v:.0%}", ha="center", va="center",
                        fontsize=8, color="white")
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    a2.set_xticks(range(len(classes)))
    a2.set_xticklabels(classes)
    a2.set_ylabel("share of misclassified")
    a2.set_title(f"Error types (decisive >= {decisive}, blind < {blind})")
    a2.legend(fontsize=8, loc="lower right")

    # (c) pooled strip
    for k, name in enumerate(("correct", "misclassified")):
        vals = pooled[name]
        xs = [(k - 1) + (float(torch.rand(1)) - 0.5) * 0.3 for _ in range(len(vals))]
        a3.scatter(xs, vals, s=16, alpha=0.7)
        a3.hlines(sum(vals) / len(vals), k - 1 - 0.2, k - 1 + 0.2, color="black", lw=2)
    a3.axhline(decisive, color="tab:red", ls="--", lw=1)
    a3.axhline(blind, color="tab:blue", ls="--", lw=1)
    a3.set_xticks([0, 1])
    a3.set_xticklabels(["correct", "misclassified"])
    a3.set_ylabel("ratio = max_drop / margin")
    a3.set_title(f"Pooled, n={len(pooled['correct'])}+{len(pooled['misclassified'])}")
    a3.grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  taxonomy -> {out_path}")


def plot_decisive(plt, cfg, model, imgs, labels, preds, ratio, idx, out_path, device):
    """input | Grad-CAM | occlusion drop, for the decisively-wrong samples."""
    import numpy as np

    if len(idx) == 0:
        print("  no decisive mistakes to show")
        return
    x = imgs[idx].to(device)
    cam, _, _ = grad_cam(model, x, "conv2")
    drop, base_prob, oc_pred, margin = occlusion_sensitivity(model, x, 8, 4)

    mean = torch.tensor(cfg["mean"]).view(1, -1, 1, 1)
    std = torch.tensor(cfg["std"]).view(1, -1, 1, 1)
    vis = (imgs[idx] * std + mean).clamp(0, 1)

    n = len(idx)
    fig, axes = plt.subplots(n, 3, figsize=(7.4, 1.95 * n))
    for r in range(n):
        i = int(idx[r])
        img = vis[r].permute(1, 2, 0).numpy().squeeze()
        base = img if img.ndim == 3 else np.stack([img] * 3, -1)
        d = drop[r].cpu().numpy()
        vmax = max(abs(d).max(), 1e-6)
        blend = (0.55 * base + 0.45 * plt.cm.bwr(d / (2 * vmax) + 0.5)[..., :3]).clip(0, 1)

        axes[r, 0].imshow(img, cmap=None if img.ndim == 3 else "gray")
        axes[r, 0].set_title(f"true {cfg['classes'][int(labels[i])]}", fontsize=9)
        axes[r, 1].imshow(cam[r].numpy(), cmap="jet")
        axes[r, 1].set_title("Grad-CAM (conv2)", fontsize=9)
        axes[r, 2].imshow(blend)
        axes[r, 2].set_title(f"pred {cfg['classes'][int(oc_pred[r])]} "
                             f"{base_prob[r]:.1%} | ratio {float(ratio[i]):.2f}", fontsize=9)
        for ax in axes[r]:
            ax.set_xticks([])
            ax.set_yticks([])
    fig.suptitle("Decisively wrong: a local cue drove the answer", fontsize=10)
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  decisive examples -> {out_path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(DATASETS), default="cifar10")
    ap.add_argument("--classes", default="bird,dog,ship",
                    help="comma separated class names or digits")
    ap.add_argument("--k", type=int, default=40, help="samples per class per group")
    ap.add_argument("--min-conf", type=float, default=0.90,
                    help="confidence band lower bound (default keeps margins comparable)")
    ap.add_argument("--max-conf", type=float, default=1.01)
    ap.add_argument("--decisive", type=float, default=0.60, help="ratio >= this = decisive")
    ap.add_argument("--blind", type=float, default=0.20, help="ratio < this = blind")
    ap.add_argument("--patch", type=int, default=8)
    ap.add_argument("--stride", type=int, default=4)
    ap.add_argument("--show", type=int, default=6, help="how many decisive mistakes to draw")
    ap.add_argument("--ckpt", default="")
    ap.add_argument("--tag", default="", help="suffix for the output filenames")
    args = ap.parse_args()

    cfg = DATASETS[args.dataset]
    classes = [c.strip() for c in args.classes.split(",") if c.strip()]
    bad = [c for c in classes if c not in cfg["classes"]]
    if bad:
        raise SystemExit(f"unknown class(es) {bad}; choose from {cfg['classes']}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    ckpt = Path(args.ckpt) if args.ckpt else RUN_ROOT / args.dataset / "best.pt"
    out_dir = ckpt.parent / "inspect"
    arch_file = ckpt.parent / "arch.txt"
    arch = arch_file.read_text(encoding="utf-8").strip() if arch_file.exists() else "small"
    out_dir.mkdir(parents=True, exist_ok=True)

    _, test_dl = get_loaders(args.dataset, r"C:\Users\princ\cnn_demo\data", 256, 0, None)
    model = build_model(cfg["in_ch"], len(cfg["classes"]), arch).to(device)
    model.load_state_dict(torch.load(ckpt, map_location=device))
    model.eval()
    print(f"loaded {ckpt} | arch {arch} | {device} | classes={classes} | k={args.k}")

    imgs, labels, preds, confs = scan_predictions(model, test_dl, device)
    overall = (preds == labels).float().mean().item()
    print(f"overall test accuracy {overall:.3f}")

    sel, meta = [], []
    for cname in classes:
        ci = cfg["classes"].index(cname)
        oc = pick_group(labels, preds, confs, ci, args.k, True,
                        min_conf=args.min_conf, max_conf=args.max_conf)
        ow = pick_group(labels, preds, confs, ci, args.k, False,
                        min_conf=args.min_conf, max_conf=args.max_conf)
        for i in oc.tolist():
            sel.append(i)
            meta.append((cname, "correct"))
        for i in ow.tolist():
            sel.append(i)
            meta.append((cname, "misclassified"))
        n_cls = int((labels == ci).sum())
        print(f"  {cname:6} {n_cls:4} images, {int(((labels == ci) & (preds != labels)).sum()):4} wrong "
              f"-> sampled {len(oc)}+{len(ow)}")

    sel_t = torch.tensor(sel)
    drop, base_prob, oc_pred, margin = occlusion_sensitivity(
        model, imgs[sel_t].to(device), args.patch, args.stride)
    ratio = (drop.amax(dim=(1, 2)) / margin.clamp(min=1e-6)).cpu()
    centre, border = centre_border_drop(drop.cpu(), imgs.shape[-1])

    stats = {}
    for cname in classes:
        idx_c = [i for i, m in enumerate(meta) if m == (cname, "correct")]
        idx_w = [i for i, m in enumerate(meta) if m == (cname, "misclassified")]
        kinds = {}
        for i in idx_w:
            kinds[classify(float(ratio[i]), args.decisive, args.blind)] = \
                kinds.get(classify(float(ratio[i]), args.decisive, args.blind), 0) + 1
        stats[cname] = {
            "correct_mean": float(ratio[idx_c].mean()) if idx_c else 0.0,
            "wrong_mean": float(ratio[idx_w].mean()) if idx_w else 0.0,
            "n_wrong": len(idx_w),
            "kinds": kinds,
            "order_wrong": idx_w,
        }

    pooled = {
        "correct": ratio[[i for i, m in enumerate(meta) if m[1] == "correct"]].tolist(),
        "misclassified": ratio[[i for i, m in enumerate(meta) if m[1] == "misclassified"]].tolist(),
    }

    plt = _pyplot()
    tag = f"_{args.tag}" if getattr(args, "tag", "") else ""
    plot_taxonomy(plt, classes, stats, pooled, args.decisive, args.blind,
                  out_dir / f"taxonomy{tag}.png")

    decisive_idx = [i for i in range(len(sel))
                    if meta[i][1] == "misclassified" and ratio[i] >= args.decisive]
    decisive_idx = sorted(decisive_idx, key=lambda i: -float(ratio[i]))[: args.show]
    plot_decisive(plt, cfg, model, imgs[sel_t], labels[sel_t], oc_pred.cpu(), ratio,
                  torch.tensor(decisive_idx), out_dir / f"decisive_wrong{tag}.png", device)

    rep = [f"dataset={args.dataset} classes={classes} k={args.k} "
           f"conf>={args.min_conf} arch={arch} overall_acc={overall:.3f}",
           f"decisive >= {args.decisive}, blind < {args.blind}", ""]
    for cname in classes:
        s = stats[cname]
        rep.append(f"{cname:6} correct_mean={s['correct_mean']:.3f} "
                   f"wrong_mean={s['wrong_mean']:.3f} "
                   f"kinds={s['kinds']}")
    allw = pooled["misclassified"]
    n_dec = sum(1 for v in allw if v >= args.decisive)
    n_blind = sum(1 for v in allw if v < args.blind)
    rep += ["",
            f"pooled correct  n={len(pooled['correct'])} mean={sum(pooled['correct']) / len(pooled['correct']):.3f}",
            f"pooled wrong    n={len(allw)} mean={sum(allw) / len(allw):.3f}",
            f"decisive wrong  {n_dec}/{len(allw)} = {n_dec / len(allw):.0%}",
            f"blind wrong     {n_blind}/{len(allw)} = {n_blind / len(allw):.0%}"]
    (out_dir / f"taxonomy{tag}.txt").write_text("\n".join(rep) + "\n", encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
