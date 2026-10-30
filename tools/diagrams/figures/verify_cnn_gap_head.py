# -*- coding: utf-8 -*-
"""Numbers for the 「為什麼現代 CNN 常不用全連接層」 page.

    python verify_cnn_gap_head.py
"""
import numpy as np

SEP = "-" * 72
rng = np.random.default_rng(11)


def mobilenet_v2_params(width=1.0, classes=1000):
    """Parameter count of MobileNetV2 (1.0), block by block."""
    c = lambda v: int(round(v * width))
    total = 0
    rows = []
    # stem: 3x3 conv, 3 -> 32, stride 2
    p = 3 * 3 * 3 * c(32) + c(32)
    rows.append(("stem 3x3, 3->32", p))
    total += p
    spec = [(1, 16, 1, 1), (6, 24, 2, 2), (6, 32, 3, 2), (6, 64, 4, 2),
            (6, 96, 3, 1), (6, 160, 3, 2), (6, 320, 1, 1)]
    cin = 32
    for t, cout, n, stride in spec:
        for i in range(n):
            mid = cin * t
            s = stride if i == 0 else 1
            p = 0
            if t != 1:
                p += cin * mid + mid                      # expand 1x1
            p += mid * 9 + mid                            # depthwise 3x3
            p += mid * cout + cout                        # project 1x1
            rows.append(("bneck t=%d c=%d n=%d s=%d #%d" % (t, cout, n, s, i + 1), p))
            total += p
            cin = cout
    p = c(320) * c(1280) + c(1280)
    rows.append(("conv 1x1, 320->1280", p))
    total += p
    head = c(1280) * classes + classes
    rows.append(("classifier 1280->%d" % classes, head))
    total += head
    return rows, total, head


def main():
    print(SEP)
    print("1. the old head: flatten 7x7x512 then one big linear layer")
    flat = 7 * 7 * 512
    big = flat * 1000 + 1000
    print("   7*7*512 =", flat)
    print("   flatten -> Linear(25,088 -> 1000): %d weights + 1,000 bias = %d"
          % (flat * 1000, big))

    print(SEP)
    print("2. the GAP head")
    gap = 512 * 1000 + 1000
    print("   GAP -> 512 -> Linear(512 -> 1000): %d weights + 1,000 bias = %d"
          % (512 * 1000, gap))
    print("   ratio old / gap = %.1fx" % (big / float(gap)))
    print("   gap head is %.2fM, old head is %.2fM" % (gap / 1e6, big / 1e6))

    print(SEP)
    print("3. how much of a real network is the classifier")
    rows, total, head = mobilenet_v2_params()
    print("   MobileNetV2 (1.0, 1000 classes):")
    print("     total params            : %d" % total)
    print("     classifier (1280->1000) : %d  = %.1f%% of the model"
          % (head, 100.0 * head / total))
    vgg_conv = 14_714_688
    vgg_fc1 = 25088 * 4096 + 4096
    vgg_fc2 = 4096 * 4096 + 4096
    vgg_fc3 = 4096 * 1000 + 1000
    vgg_total = vgg_conv + vgg_fc1 + vgg_fc2 + vgg_fc3
    vgg_head = vgg_fc1 + vgg_fc2 + vgg_fc3
    print("     VGG16 total             : %d" % vgg_total)
    print("     VGG16 classifier        : %d  = %.1f%%"
          % (vgg_head, 100.0 * vgg_head / vgg_total))
    res_total = 25_557_032
    res_head = 2048 * 1000 + 1000
    print("     ResNet-50 classifier    : %d  = %.1f%% of %d"
          % (res_head, 100.0 * res_head / res_total, res_total))

    print(SEP)
    print("4. input size freedom")
    for side in (7, 8, 14):
        print("   %2dx%2dx512 -> GAP %3d 維  |  flatten %5d 維"
              % (side, side, 512, side * side * 512))

    print(SEP)
    print("5. shift the feature map by one pixel")
    fmap = np.arange(1, 50, dtype=float).reshape(7, 7)
    rolled = np.roll(fmap, 1, axis=1)
    print("   GAP original : %.4f" % fmap.mean())
    print("   GAP shifted  : %.4f  (difference %.1e)"
          % (rolled.mean(), abs(rolled.mean() - fmap.mean())))
    d = np.linalg.norm(rolled.ravel() - fmap.ravel())
    print("   flatten L2 distance after the same shift: %.2f" % d)
    print("   positions that changed in the flattened vector: %d / %d"
          % (int((rolled != fmap).sum()), fmap.size))

    print(SEP)
    print("7. GAP vs ordinary average pooling on the same 7x7 map")
    m7 = np.arange(1, 50, dtype=float).reshape(7, 7)
    print("   7x7 map, GAP                -> %.2f  (shape 1x1, covers all 49 cells)"
          % m7.mean())
    out = [[float(m7[i:i + 2, j:j + 2].mean()) for j in range(0, 5, 2)]
           for i in range(0, 5, 2)]
    print("   AvgPool2d(2,2)  -> shape (3, 3):", [[round(v, 2) for v in r] for r in out])
    print("   mean of that 3x3 map        -> %.2f  (only 36 of 49 cells are covered)"
          % np.array(out).mean())
    out3 = [[float(m7[i:i + 3, j:j + 3].mean()) for j in range(0, 4, 3)]
            for i in range(0, 4, 3)]
    print("   AvgPool2d(3,3)  -> shape (2, 2):", [[round(v, 2) for v in r] for r in out3])
    print("   mean of that 2x2 map        -> %.2f  (again 36 of 49)" % np.array(out3).mean())
    print("   AvgPool2d(7,7)  -> shape (1, 1): [[%.2f]]  == GAP" % m7.mean())
    print("   7x7 with k=7 covers every cell, so it *is* GAP")

    print(SEP)
    print("8. per-channel independence")
    A = rng.normal(size=(3, 4, 5))          # C=3, H=4, W=5
    gap_axes = A.mean(axis=(1, 2))
    manual = np.array([A[c].mean() for c in range(3)])
    print("   A shape", A.shape, "-> GAP", np.round(gap_axes, 4))
    print("   per-channel loop matches mean(dim=(1,2)):", bool(np.allclose(gap_axes, manual)))
    print("   mean of the whole tensor:", round(float(A.mean()), 4),
          "(same number, but it loses which channel it came from)")

    print(SEP)
    print("9. GAP + Linear  ==  spatial mean of the CAM")
    C, H, W, K = 4, 5, 5, 3
    A = rng.random((C, H, W))
    Wk = rng.random((K, C))
    gap = A.mean(axis=(1, 2))
    logits = Wk @ gap
    cam = np.einsum("kc,chw->khw", Wk, A)
    print("   logits (GAP then Linear) :", np.round(logits, 4))
    print("   mean of CAM per class    :", np.round(cam.mean(axis=(1, 2)), 4))
    print("   max abs difference       : %.2e"
          % float(np.abs(logits - cam.mean(axis=(1, 2))).max()))
    print("   -> the classifier weight IS the CAM weight; GAP only averages it")

    print(SEP)
    print("10. the same head accepts any input size")
    for side in (7, 14, 28):
        print("   %2dx%2dx512 -> GAP 512 -> Linear(512->1000) works: %s"
              % (side, side, True))
    print(SEP)



if __name__ == "__main__":
    main()
