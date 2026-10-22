r"""
confusion_probe.py -- confusion matrix + "who gets mistaken for whom" rates.

The point of this probe is to measure ONE specific shortcut quantitatively, e.g.
"what fraction of birds is predicted as plane?", before and after a targeted fix
(large-area RandomErasing). Precision beats anecdotes.

Outputs (<ckpt dir>\inspect\):
    confusion.png   row-normalised confusion matrix with counts
    confusion.txt   the same numbers, plus the top off-diagonal confusions

Usage:
  python confusion_probe.py --ckpt run_wide\cifar10\best.pt --class bird
"""
import argparse
from pathlib import Path

import torch

from inspect_model import scan_predictions
from train_cnn import DATASETS, _pyplot, build_model, get_loaders

RUN_ROOT = Path(r"C:\Users\princ\cnn_demo\run")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(DATASETS), default="cifar10")
    ap.add_argument("--ckpt", default="")
    ap.add_argument("--class", dest="cls", default="", help="focus class (optional)")
    ap.add_argument("--tag", default="")
    args = ap.parse_args()

    cfg = DATASETS[args.dataset]
    classes = list(cfg["classes"])
    ckpt = Path(args.ckpt) if args.ckpt else RUN_ROOT / args.dataset / "best.pt"
    out_dir = ckpt.parent / "inspect"
    out_dir.mkdir(parents=True, exist_ok=True)
    arch_file = ckpt.parent / "arch.txt"
    arch = arch_file.read_text(encoding="utf-8").strip() if arch_file.exists() else "small"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    _, test_dl = get_loaders(args.dataset, r"C:\Users\princ\cnn_demo\data", 256, 0, None)
    model = build_model(cfg["in_ch"], len(classes), arch).to(device)
    model.load_state_dict(torch.load(ckpt, map_location=device))
    model.eval()

    _, labels, preds, _ = scan_predictions(model, test_dl, device)
    n = len(classes)
    cm = torch.zeros(n, n, dtype=torch.long)
    for t, p in zip(labels.tolist(), preds.tolist()):
        cm[t, p] += 1
    acc = (labels == preds).float().mean().item()
    rown = cm.float() / cm.sum(1, keepdim=True).clamp(min=1)
    print(f"loaded {ckpt} | arch {arch} | overall acc {acc:.4f}")

    plt = _pyplot()
    fig, ax = plt.subplots(figsize=(7.8, 6.8))
    im = ax.imshow(rown.numpy(), cmap="Blues", vmin=0, vmax=1)
    for i in range(n):
        for j in range(n):
            v = float(rown[i, j])
            if v >= 0.01:
                ax.text(j, i, f"{v * 100:.0f}\n({int(cm[i, j])})", ha="center", va="center",
                        fontsize=6.5, color="white" if v > 0.55 else "black")
    ax.set_xticks(range(n))
    ax.set_xticklabels(classes, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(n))
    ax.set_yticklabels(classes, fontsize=8)
    ax.set_xlabel("predicted")
    ax.set_ylabel("true")
    ax.set_title(f"Confusion matrix (%) - acc {acc:.3f} | {ckpt.parent.name}/{arch}")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    fig.tight_layout()
    tag = f"_{args.tag}" if args.tag else ""
    fig.savefig(out_dir / f"confusion{tag}.png", dpi=130)
    plt.close(fig)
    print(f"  confusion -> {out_dir / f'confusion{tag}.png'}")

    lines = [f"ckpt={ckpt} arch={arch} acc={acc:.4f}", ""]
    focus = [args.cls] if args.cls else classes
    for cname in focus:
        if cname not in classes:
            raise SystemExit(f"unknown class {cname!r}; choose from {classes}")
        i = classes.index(cname)
        total = int(cm[i].sum())
        order = torch.argsort(rown[i], descending=True).tolist()
        parts = [f"{classes[j]}={float(rown[i, j]) * 100:.1f}%({int(cm[i, j])})"
                 for j in order[:5]]
        lines.append(f"{cname:6} n={total:4} acc={float(rown[i, i]) * 100:5.1f}% | top: " + ", ".join(parts))
    off = [(float(rown[i, j]), classes[i], classes[j]) for i in range(n) for j in range(n) if i != j]
    off.sort(reverse=True)
    lines += ["", "biggest off-diagonal confusions:"]
    lines += [f"  {t} -> {p}: {v * 100:.1f}%" for v, t, p in off[:8]]
    (out_dir / f"confusion{tag}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
