"""
cnn_check.py -- validate the CNN snippet from the notes.

Checks:
  1. the exact nn.Sequential from the notes: output shape + params per layer
  2. where 64*8*8 comes from (spatial size bookkeeping)
  3. what breaks if padding=1 is removed
  4. what breaks if the input is 224x224 instead of 32x32
  5. an improved variant: BatchNorm + Global Average Pooling (resolution agnostic)
  6. a short training smoke test on synthetic data (does loss actually drop?)

Run:
  C:\\Users\\princ\\miniconda3\\envs\\gpu\\python.exe C:\\Users\\princ\\cnn_demo\\cnn_check.py
"""
import time

import torch
import torch.nn as nn


def n_params(m: nn.Module) -> int:
    return sum(p.numel() for p in m.parameters())


def report(name: str, model: nn.Module, x: torch.Tensor, device: torch.device) -> torch.Tensor:
    """Print per-layer output shape (via forward hooks) and param counts."""
    model = model.to(device)
    shapes = []
    hooks = []
    for layer in model:
        hooks.append(
            layer.register_forward_hook(lambda m, i, o, buf=shapes: buf.append((m, o.shape)))
        )
    model.eval()
    with torch.no_grad():
        y = model(x.to(device))
    for h in hooks:
        h.remove()

    print(f"\n=== {name} ===")
    print(f"input         : {tuple(x.shape)}")
    for layer, shape in shapes:
        kind = type(layer).__name__
        extra = f"{tuple(layer.weight.shape)}" if isinstance(layer, (nn.Conv2d, nn.Linear)) else ""
        print(f"{kind:<16}: {shape}  {extra}")
    print(f"output        : {tuple(y.shape)}")
    print(f"total params  : {n_params(model):,}")
    return y


def main() -> None:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("torch", torch.__version__, "| device", device)

    # ---------- 1. the snippet exactly as written in the notes ----------
    baseline = nn.Sequential(
        nn.Conv2d(3, 32, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),

        nn.Conv2d(32, 64, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),

        nn.Flatten(),
        nn.Linear(64 * 8 * 8, 128),
        nn.ReLU(),
        nn.Linear(128, 10),
    )
    x32 = torch.randn(1, 3, 32, 32)
    report("baseline (32x32, padding=1)", baseline, x32, device)

    print("\nper-layer params:")
    for name, mod in baseline.named_children():
        if n_params(mod):
            print(f"  {name:<10} {type(mod).__name__:<10} {n_params(mod):>9,}")

    # ---------- 2. spatial bookkeeping: where does 8 come from ----------
    print("\nspatial size trace (32 -> 32 -> 16 -> 16 -> 8):")
    s = 32
    print(f"  input        {s}")
    for layer in baseline:
        if isinstance(layer, (nn.Conv2d, nn.MaxPool2d)):
            k = layer.kernel_size if isinstance(layer.kernel_size, int) else layer.kernel_size[-1]
            pad = getattr(layer, "padding", 0)
            pad = pad if isinstance(pad, int) else pad[-1]
            stride = layer.stride if isinstance(layer.stride, int) else layer.stride[-1]
            s = (s + 2 * pad - k) // stride + 1
            print(f"  {type(layer).__name__:<10} {s}")
    print(f"  Flatten      {64} * {s} * {s} = {64 * s * s}")


    # ---------- 3. without padding ----------
    no_pad = nn.Sequential(
        nn.Conv2d(3, 32, kernel_size=3),  # no padding now
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(32, 64, kernel_size=3),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Flatten(),
        nn.Linear(64 * 8 * 8, 128),       # kept the notes' number -> mismatch
        nn.ReLU(),
        nn.Linear(128, 10),
    )
    print("\n=== padding removed, Linear still 64*8*8 ===")
    try:
        no_pad(x32)
    except RuntimeError as e:
        print("RuntimeError:", e)

    # ---------- 4. same model, 224x224 input ----------
    print("\n=== baseline with 224x224 input ===")
    try:
        baseline(torch.randn(1, 3, 224, 224).to(device))
    except RuntimeError as e:
        print("RuntimeError:", str(e)[:200], "...")

    # ---------- 5. improved variant: BN + GAP (any input size >= 8) ----------
    improved = nn.Sequential(
        nn.Conv2d(3, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(),
        nn.MaxPool2d(2),

        nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
        nn.MaxPool2d(2),

        nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(),
        nn.AdaptiveAvgPool2d(1),      # -> (B,128,1,1): works for ANY input size
        nn.Flatten(),
        nn.Dropout(0.2),
        nn.Linear(128, 10),
    )
    report("improved (BN + GAP)", improved, x32, device)
    print("  same model, 64x64 input  ->", tuple(improved(torch.randn(1, 3, 64, 64).to(device)).shape))
    print("  same model, 224x224 input->", tuple(improved(torch.randn(1, 3, 224, 224).to(device)).shape))

    # ---------- 6. does it actually train? synthetic 3-class blobs ----------
    print("\n=== training smoke test (synthetic data, 3 classes) ===")
    torch.manual_seed(0)
    n = 600
    # 3 "classes" = a bright blob in three different places
    y_true = torch.randint(0, 3, (n,))
    xb = torch.randn(n, 3, 32, 32) * 0.3
    for c in range(3):
        mask = y_true == c
        xb[mask, c, 4 + 8 * c: 14 + 8 * c, 4 + 8 * c: 14 + 8 * c] += 2.0
    xb = xb.to(device)
    yb = y_true.to(device)

    net = improved.to(device)
    opt = torch.optim.Adam(net.parameters(), lr=3e-3)
    loss_fn = nn.CrossEntropyLoss()

    t0 = time.time()
    net.train()
    for epoch in range(1, 13):
        perm = torch.randperm(n, device=device)
        total = 0.0
        for i in range(0, n, 64):
            idx = perm[i: i + 64]
            opt.zero_grad()
            loss = loss_fn(net(xb[idx]), yb[idx])
            loss.backward()
            opt.step()
            total += loss.item() * len(idx)
        if epoch in (1, 4, 8, 12):
            net.eval()
            with torch.no_grad():
                acc = (net(xb).argmax(1) == yb).float().mean().item()
            print(f"  epoch {epoch:>2}  loss {total / n:.4f}  train acc {acc:.3f}")
            net.train()
    print(f"  {time.time() - t0:.1f}s on {device}")

    print("\nOK: all checks ran.")
    print("note: the models above are randomly initialised unless trained;"
          " untrained predictions mean nothing.")


if __name__ == "__main__":
    main()
