# -*- coding: utf-8 -*-
"""Every number on the 卷積層的運作細節 page is computed here first.

    python verify_cnn_conv_details.py
"""
import numpy as np

SEP = "-" * 72


def out_size(w, k, s=1, p=0, d=1):
    return (w + 2 * p - d * (k - 1) - 1) // s + 1


def conv2d(img, ker, stride=1, pad=0, dil=1, bias=0):
    H, W = img.shape
    f = ker.shape[0]
    if pad:
        img = np.pad(img, pad, mode="constant")
    ho = (img.shape[0] - (dil * (f - 1) + 1)) // stride + 1
    wo = (img.shape[1] - (dil * (f - 1) + 1)) // stride + 1
    out = np.zeros((ho, wo), dtype=int)
    for i in range(ho):
        for j in range(wo):
            patch = img[i * stride:i * stride + dil * (f - 1) + 1:dil,
                        j * stride:j * stride + dil * (f - 1) + 1:dil]
            out[i, j] = int((patch * ker).sum()) + bias
    return out


def main():
    # ---- the worked example used on the page ------------------------------
    x = np.array([[1, 2, 3, 0, 1],
                  [0, 1, 2, 3, 1],
                  [2, 0, 1, 1, 0],
                  [1, 2, 0, 3, 1],
                  [0, 1, 1, 2, 0]])
    k = np.array([[1, 0, 1],
                  [0, 1, 0],
                  [1, 0, 1]])
    fmap = conv2d(x, k)
    print(SEP)
    print("1. 5x5 input, 3x3 kernel, stride 1, no padding, bias 0")
    print("   input:\n", x)
    print("   top-left 3x3:\n", x[:3, :3])
    print("   kernel:\n", k)
    print("   feature map:\n", fmap)
    print("   top-left cell =", fmap[0, 0])
    print("   with bias 1  =", conv2d(x, k, bias=1)[0, 0])

    # ---- output size, 28x28 with a 3x3 kernel -----------------------------
    print(SEP)
    print("2. output size  O = floor((W + 2P - d(k-1) - 1) / S) + 1")
    for name, w, kk, s, p in [("28,3x3,s1,pad0 (valid)", 28, 3, 1, 0),
                              ("28,3x3,s1,pad1 (same)", 28, 3, 1, 1),
                              ("28,3x3,s2,pad1", 28, 3, 2, 1),
                              ("28,5x5,s1,pad2 (same)", 28, 5, 1, 2),
                              ("28,3x3,s2,pad0", 28, 3, 2, 0)]:
        print("   %-28s -> %d" % (name, out_size(w, kk, s, p)))

    # ---- dilation ---------------------------------------------------------
    print(SEP)
    print("3. dilated kernel footprint  k_eff = d(k-1) + 1")
    for d in (1, 2, 3, 4):
        print("   3x3, d=%d -> footprint %d (weights still 9)" % (d, d * 2 + 1))
    for d in (1, 2):
        print("   28x28, 3x3, d=%d, s1, pad0 -> out %d"
              % (d, out_size(28, 3, 1, 0, d)))
    print("   28x28, 3x3, d=2, s1, pad2 -> out %d" % out_size(28, 3, 1, 2, 2))

    # ---- parameter counts -------------------------------------------------
    print(SEP)
    print("4. parameter counts   (k*k*C_in + 1) * C_out")
    for cin, cout, kk in ((3, 64, 3), (3, 1, 3), (16, 32, 3), (1, 6, 5)):
        w = kk * kk * cin
        print("   %dx%d, C_in=%d, C_out=%d -> weights %d + bias %d = %d"
              % (kk, kk, cin, cout, w * cout, cout, w * cout + cout))

    # ---- receptive field --------------------------------------------------
    print(SEP)
    print("5. receptive field, stacked 3x3 stride 1")
    rf, jump = 1, 1
    for layer in range(1, 5):
        rf += (3 - 1) * jump
        print("   after layer %d: %d x %d" % (layer, rf, rf))
    print("   same stack, every layer stride 2:")
    rf, jump = 1, 1
    for layer in range(1, 5):
        rf += (3 - 1) * jump
        jump *= 2
        print("   after layer %d: rf %d, jump %d" % (layer, rf, jump))

    # ---- one channel sum --------------------------------------------------
    print(SEP)
    print("6. multi-channel kernel: 3 channels summed into one value")
    chans = [np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
             np.array([[2, 0, 1], [1, 0, 2], [0, 1, 0]]),
             np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])]
    kers = [np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]]),
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
            np.array([[0, -1, 0], [-1, 0, -1], [0, -1, 0]])]
    per = [int((c * kk).sum()) for c, kk in zip(chans, kers)]
    print("   per-channel sums:", per, "-> total", sum(per),
          "| + bias 2 =", sum(per) + 2)
    print(SEP)


if __name__ == "__main__":
    main()
