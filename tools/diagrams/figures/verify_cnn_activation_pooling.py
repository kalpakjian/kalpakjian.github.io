# -*- coding: utf-8 -*-
"""Every number on the 激活函數與池化層 page is computed here first.

    python verify_cnn_activation_pooling.py
"""
import numpy as np

SEP = "-" * 72
rng = np.random.default_rng(7)


def relu(x):
    return np.maximum(0.0, x)


def leaky(x, a=0.1):
    return np.where(x > 0, x, a * x)


def gelu(x):
    return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * x ** 3)))


def maxpool(x, k=2, s=2, p=0):
    x = np.asarray(x, dtype=float)
    if p:
        x = np.pad(x, p, constant_values=-np.inf)
    H, W = x.shape
    ho, wo = (H - k) // s + 1, (W - k) // s + 1
    out = np.zeros((ho, wo))
    arg = np.zeros((ho, wo), dtype=tuple)
    for i in range(ho):
        for j in range(wo):
            win = x[i * s:i * s + k, j * s:j * s + k]
            m = np.unravel_index(int(np.argmax(win)), win.shape)
            out[i, j] = win[m]
            arg[i, j] = (int(i * s + m[0] - p), int(j * s + m[1] - p))
    return out, arg


def maxpool_backward(grad, arg, shape):
    """Route each upstream gradient only to the cell that won its window."""
    g = np.zeros(shape)
    for idx in np.ndindex(grad.shape):
        g[arg[idx]] += grad[idx]
    return g


def main():
    v = np.array([-3.0, -1.0, 0.0, 0.5, 2.0])
    print(SEP)
    print("1. ReLU and its variants on the same input", v)
    print("   ReLU      :", relu(v))
    print("   Leaky 0.1 :", np.round(leaky(v), 3))
    print("   Leaky 0.01:", np.round(leaky(v, 0.01), 3))
    print("   GELU      :", np.round(gelu(v), 4))
    for x in (-3.0, -1.0, -0.1, 0.1, 3.0):
        print("   x=%5.1f  relu=%.3f  leaky=%.3f  gelu=%.4f"
              % (x, relu(np.array([x]))[0], leaky(np.array([x]))[0], gelu(np.array([x]))[0]))

    print(SEP)
    print("2. two linear layers == one linear layer")
    W1 = rng.normal(size=(4, 5))
    b1 = rng.normal(size=4)
    W2 = rng.normal(size=(3, 4))
    b2 = rng.normal(size=3)
    x = rng.normal(size=(2, 5))
    deep = (W1 @ x.T + b1[:, None])
    deep = W2 @ deep + b2[:, None]
    flat = (W2 @ W1) @ x.T + (W2 @ b1 + b2)[:, None]
    print("   max |deep - flat| =", float(np.abs(deep - flat).max()))

    print(SEP)
    print("3. how sparse is a ReLU feature map?  (N(0,1) input, 1000x1000)")
    big = rng.normal(size=(1000, 1000))
    print("   zeros after ReLU: %.1f%%" % (100.0 * (relu(big) == 0).mean()))
    print("   zeros, standard normal: %.1f%% (theory 50%%)"
          % (100.0 * (relu(big) == 0).mean()))

    print(SEP)
    print("4. a dead unit: bias so negative that every input is clipped")
    w = rng.normal(size=256)
    feats = rng.normal(size=(512, 256))
    proj = feats @ w
    print("   max projection over 512 samples: %.2f" % float(proj.max()))
    for bias in (0.0, round(float(proj.max()) / 2, 2), round(float(proj.max()) + 1, 2)):
        z = proj - bias
        print("   bias %8.2f -> all outputs zero? %-5s  (max %.2f)"
              % (bias, bool((relu(z) == 0).all()), float(z.max())))

    print(SEP)
    print("5. pooling, the example used on the page")
    m = np.array([[1, 1, 2, 4],
                  [5, 6, 7, 8],
                  [3, 2, 1, 0],
                  [1, 2, 3, 4]])
    out, arg = maxpool(m)
    print("   input:\n", m)
    print("   2x2 max, stride 2 ->\n", out.astype(int))
    print("   winners (row,col):", arg.tolist())
    quads = [m[0:2, 0:2], m[0:2, 2:4], m[2:4, 0:2], m[2:4, 2:4]]
    print("   average pooling  ->", [round(float(q.mean()), 2) for q in quads])
    print("   values 16 -> 4, reduction %.0f%%" % (100.0 * (1 - 4 / 16.0)))

    win = np.array([[2, 7], [1, 5]])
    print("   one window [2 7; 1 5]: max %d, avg %.2f" % (win.max(), win.mean()))

    print(SEP)
    print("6. pooling output size  O = floor((W - k + 2p)/s) + 1")
    for name, w0, k, s, p in [("4, k2, s2, pad0", 4, 2, 2, 0),
                              ("4, k2, s1, pad0 (overlap)", 4, 2, 1, 0),
                              ("4, k3, s2, pad1", 4, 3, 2, 1),
                              ("28, k2, s2, pad0", 28, 2, 2, 0),
                              ("7, k7, s1, pad0 (global)", 7, 7, 1, 0)]:
        print("   %-26s -> %d" % (name, (w0 - k + 2 * p) // s + 1))
    overlap, _ = maxpool(m, k=2, s=1)
    print("   overlap pooling on the 4x4 map ->\n", overlap.astype(int))
    padded, _ = maxpool(m, k=3, s=2, p=1)
    print("   k3 s2 pad1 (pad with -inf) ->\n", padded.astype(int))

    print(SEP)
    print("7. max-pool backward: the gradient only goes to the winner")
    grad = np.array([[1.0, 2.0], [3.0, 4.0]])
    g = maxpool_backward(grad, arg, m.shape)
    print("   upstream grad:\n", grad)
    print("   grad on the input map:\n", g.astype(int))
    print("   sum preserved:", float(g.sum()), "==", float(grad.sum()))
    # finite-difference check: d(sum(w*pool(x)))/dx must equal the routed grad
    wts = grad

    def loss(scale):
        return float((wts * maxpool(m.astype(float) * scale)[0]).sum())

    eps = 1e-4
    fd = np.zeros(m.shape)
    for idx in np.ndindex(m.shape):
        e = np.zeros(m.shape)
        e[idx] = eps
        fd[idx] = (loss(1.0 + 0.0) if False else
                   float((wts * maxpool(m.astype(float) + e)[0]).sum())
                   - float((wts * maxpool(m.astype(float) - e)[0]).sum())) / (2 * eps)
    print("   finite-difference grad matches routed grad:",
          bool(np.allclose(fd, g, atol=1e-6)))

    print(SEP)
    print("8. one CNN block, shape by shape (the example on the page)")
    print("   input            32 x 32 x 3")
    print("   Conv 3x3 x32 pad1  32 x 32 x 32  params (27+1)*32 =", (27 + 1) * 32)
    print("   ReLU             32 x 32 x 32   params 0")
    print("   MaxPool 2x2 s2   16 x 16 x 32   params 0")
    print("   GAP on 7x7x512 -> 512           params 0")
    print(SEP)


if __name__ == "__main__":
    main()
