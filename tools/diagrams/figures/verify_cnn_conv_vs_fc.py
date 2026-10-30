# -*- coding: utf-8 -*-
"""Numbers for the 卷積層 vs 全連接層 comparison page.

    python verify_cnn_conv_vs_fc.py
"""
import numpy as np

SEP = "-" * 72


def main():
    print(SEP)
    print("1. the same job, two layers: produce 28x28x32 = 25,088 values")
    outs = 28 * 28 * 32
    conv_w = 3 * 3 * 1 * 32
    conv_b = 32
    fc_w = 784 * outs
    fc_b = outs
    print("   outputs            :", outs)
    print("   conv 3x3, C_out 32 : %d weights + %d bias = %d" % (conv_w, conv_b,
                                                                conv_w + conv_b))
    print("   fc 784 -> %-8d : %d weights + %d bias = %d" % (outs, fc_w, fc_b,
                                                              fc_w + fc_b))
    print("   ratio (total)      : %.0fx" % ((fc_w + fc_b) / float(conv_w + conv_b)))
    print("   ratio (weights)    : %.0fx" % (fc_w / float(conv_w)))

    print(SEP)
    print("2. the draft's pair (288 vs 100,352) is not apples to apples")
    print("   conv 3x3x1x32 weights only : 288  -> keeps 25,088 outputs")
    print("   fc 784 -> 128 weights only : 100,352 -> gives 128 outputs")
    print("   per-output weights: conv %.4f, fc %.1f"
          % (conv_w / float(outs), 100352 / 128.0))

    print(SEP)
    print("3. multiply-accumulates (the compute side)")
    conv_mac = outs * 9
    fc_mac = outs * 784
    print("   conv : 25,088 outputs x 9 taps   = %d MACs" % conv_mac)
    print("   fc   : 25,088 outputs x 784 taps = %d MACs" % fc_mac)
    print("   fc / conv = %.1fx more compute for %.0fx more parameters"
          % (fc_mac / float(conv_mac), (fc_w + fc_b) / float(conv_w + conv_b)))

    print(SEP)
    print("4. scaling with input size (fc  -> 128 outputs, conv 3x3 -> 32 ch)")
    print("   %-8s %14s %14s" % ("side", "fc 784-scale", "conv params"))
    base = 28
    for side in (28, 56, 112, 224, 448):
        fc = (side * side) * 128 + 128
        print("   %-8d %14d %14d" % (side, fc, 3 * 3 * 1 * 32 + 32))
    print("   28 -> 224 makes the fc layer %.0fx bigger, conv stays the same"
          % (((224 * 224) * 128 + 128) / float((28 * 28) * 128 + 128)))

    print(SEP)
    print("5. translation: one 3x3 detector on a 5x5 input (9 positions)")
    print("   conv: 9 shared weights detect the pattern anywhere -> 9 weights")
    print("   fc  : one weight per (position, pattern cell) -> 9 x 9 = 81 weights")
    print("   ratio: %.0fx" % (81 / 9.0))
    img = np.zeros((5, 5), dtype=int)
    pat = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
    for (r, c) in ((0, 0), (2, 2)):
        img[:] = 0
        img[r:r + 3, c:c + 3] = pat
        # same kernel, different position -> same peak value
        peaks = []
        for i in range(3):
            for j in range(3):
                peaks.append(int((img[i:i + 3, j:j + 3] * pat).sum()))
        print("   pattern at (%d,%d): max response %d (same kernel everywhere)"
              % (r, c, max(peaks)))

    print(SEP)
    print("6. what the two layers do to the same feature map")
    fmap = np.arange(1, 17).reshape(4, 4)
    print("   input 4x4:\n", fmap)
    print("   global average (GAP) ->", round(float(fmap.mean()), 3),
          "(1 value, 0 params)")
    print("   flatten -> 16 values, then fc 16 -> 3 : params", 16 * 3 + 3)
    print(SEP)


if __name__ == "__main__":
    main()
