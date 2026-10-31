# -*- coding: utf-8 -*-
"""Every number that appears on the 圖解 CNN page is computed here first.

    python verify_numbers.py

Nothing is hand-typed into the page: run this, paste the printed values.
"""
import numpy as np

np.set_printoptions(suppress=True, precision=4)

SEP = "-" * 72


def out_size(n, f, s=1, p=0):
    return (n + 2 * p - f) // s + 1


def main():
    # ---- 1. the worked convolution example (same numbers as cnn-notes) ------
    x = np.array([[1, 1, 1, 0, 0],
                  [0, 1, 1, 1, 0],
                  [0, 0, 1, 1, 1],
                  [0, 0, 1, 1, 0],
                  [0, 1, 1, 0, 0]])
    k = np.array([[1, 0, 1],
                  [0, 1, 0],
                  [1, 0, 1]])

    def conv2d(img, ker, stride=1):
        H, W = img.shape
        f = ker.shape[0]
        ho, wo = (H - f) // stride + 1, (W - f) // stride + 1
        out = np.zeros((ho, wo), dtype=int)
        for i in range(ho):
            for j in range(wo):
                patch = img[i * stride:i * stride + f, j * stride:j * stride + f]
                out[i, j] = int((patch * ker).sum())
        return out

    fmap = conv2d(x, k)
    print(SEP)
    print("1. conv 5x5 * 3x3 (stride 1, no padding)")
    print("   input patch top-left:")
    print(np.array2string(x[:3, :3], separator=" "))
    print("   kernel:")
    print(np.array2string(k, separator=" "))
    print("   feature map:\n", fmap)
    print("   top-left cell:", fmap[0, 0],
          "= (1*1+0*1+1*1) + (0*0+1*1+0*1) + (1*0+0*0+1*1)")

    # ---- 2. output size formula across the three classic settings ---------
    print(SEP)
    print("2. output size  O = (N + 2P - F)/S + 1")
    for name, n, f, s, p in [("valid    N=5 F=3 S=1 P=0", 5, 3, 1, 0),
                             ("same     N=5 F=3 S=1 P=1", 5, 3, 1, 1),
                             ("stride2  N=5 F=3 S=2 P=0", 5, 3, 2, 0),
                             ("MNIST    N=28 F=3 S=1 P=1", 28, 3, 1, 1),
                             ("MNIST    N=28 F=2 S=2 P=0 (pool)", 28, 2, 2, 0)]:
        print("   %-34s -> %d" % (name, out_size(n, f, s, p)))

    # ---- 3. the MNIST-shaped pipeline used by the last figure -------------
    print(SEP)
    print("3. one small MNIST CNN, shape by shape")
    stage = [("輸入", 28, 28, 1), ("Conv 3x3 x8", 28, 28, 8),
             ("Pool 2x2", 14, 14, 8), ("Conv 3x3 x16", 14, 14, 16),
             ("Pool 2x2", 7, 7, 16)]
    for name, h, w, c in stage:
        print("   %-14s %2d x %2d x %2d" % (name, h, w, c))
    flat = 7 * 7 * 16
    print("   Flatten        %d 維" % flat)
    print("   Dense 64       %d 維 (params %d)" % (64, flat * 64 + 64))
    print("   Softmax 10     10 維")

    # ---- 4. ReLU ----------------------------------------------------------
    v = np.array([-3.0, -1.0, -0.25, 0.0, 0.5, 2.0])
    print(SEP)
    print("4. ReLU(x) = max(0, x)")
    print("   in :", v)
    print("   out:", np.maximum(0, v))

    # ---- 5. max / average pooling 4x4 -> 2x2 ------------------------------
    m = np.array([[1, 3, 2, 4],
                  [5, 6, 7, 8],
                  [3, 2, 1, 0],
                  [1, 4, 9, 5]])
    quads = [m[0:2, 0:2], m[0:2, 2:4], m[2:4, 0:2], m[2:4, 2:4]]
    print(SEP)
    print("5. pooling 4x4 -> 2x2 (window 2x2, stride 2)")
    print("   input:\n", m)
    print("   max:", [int(q.max()) for q in quads])
    print("   avg:", [round(float(q.mean()), 2) for q in quads])
    print("   params:", 0)

    # ---- 6. softmax on three logits (the 'dog / cat / bird' row) ----------
    logits = np.array([4.2, 1.3, 0.4])
    e = np.exp(logits - logits.max())
    p = e / e.sum()
    print(SEP)
    print("6. softmax of logits", logits)
    print("   probabilities:", np.round(p, 4), " sum =", round(float(p.sum()), 6))

    # ---- 7. parameter counts ---------------------------------------------
    print(SEP)
    print("7. parameter counts")
    conv = (3 * 3 * 3 + 1) * 64
    dense = (7 * 7 * 64 + 1) * 10
    print("   Conv 3x3x3 -> 64 :", conv)
    print("   Dense 3136 -> 10 :", dense, " (x%.1f)" % (dense / conv))
    fc_big = (1024 + 1) * 120
    conv_small = 5 * 5 * 1
    print("   FC 1024->120     :", fc_big, " vs 5x5 conv:", conv_small,
          " (x%d)" % round(fc_big / conv_small))

    # LeNet-5, the layer-by-layer total the site already quotes
    c1 = 5 * 5 * 1 * 6 + 6
    s2 = 6 * 2
    c3 = 5 * 5 * 6 * 16 + 16
    s4 = 16 * 2
    c5 = 5 * 5 * 16 * 120 + 120
    f6 = 120 * 84 + 84
    out = 84 * 10 + 10
    print("   LeNet-5 C1=%d S2=%d C3=%d S4=%d C5=%d F6=%d out=%d"
          % (c1, s2, c3, s4, c5, f6, out))
    print("   LeNet-5 conv+fc total =", c1 + c3 + c5 + f6 + out)
    print("   LeNet-5 incl. trainable pooling =", c1 + s2 + c3 + s4 + c5 + f6 + out)

    # ---- 8. three filters on the same 5x5 image --------------------------
    kernels = {
        "vertical": np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]]),
        "diagonal": np.array([[0, 1, 0], [1, 0, -1], [0, -1, 0]]),
        "blob": np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]),
    }
    print(SEP)
    print("8. three filters, same 5x5 input -> three 3x3 maps")
    for name, ker in kernels.items():
        print("   %-9s" % name, conv2d(x, ker).tolist())
    print(SEP)


if __name__ == "__main__":
    main()
