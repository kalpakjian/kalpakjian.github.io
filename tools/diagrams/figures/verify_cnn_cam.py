# -*- coding: utf-8 -*-
"""Numbers for the CAM page (GAP → CAM → Grad-CAM).

    python verify_cnn_cam.py
"""
import numpy as np

SEP = "-" * 72
rng = np.random.default_rng(23)


def main():
    A = [np.array([[10, 0], [8, 2]], dtype=float),
         np.array([[1, 1], [1, 1]], dtype=float),
         np.array([[0, 2], [0, 2]], dtype=float)]
    w = np.array([0.8, 0.1, -0.2])

    print(SEP)
    print("1. the worked example on the page (3 maps, 2x2)")
    F = np.array([a.mean() for a in A])
    for k, (a, f) in enumerate(zip(A, F), start=1):
        print("   A%d = %s  ->  F%d = %.2f" % (k, a.tolist(), k, f))
    print("   w =", w)
    y = float(w @ F)
    print("   logit = w1F1 + w2F2 + w3F3 = %.2f" % y)

    print(SEP)
    print("2. the CAM for the same example")
    M = sum(wk * a for wk, a in zip(w, A))
    print("   M = 0.8A1 + 0.1A2 - 0.2A3 =\n", np.round(M, 2))
    print("   corner (1,1) = 0.8*10 + 0.1*1 - 0.2*0   = %.1f" % M[0, 0])
    print("   corner (1,2) = 0.8*0  + 0.1*1 - 0.2*2   = %.1f" % M[0, 1])
    print("   mean(CAM)   = %.4f   == logit %.4f  ->  %s"
          % (M.mean(), y, bool(np.isclose(M.mean(), y))))
    print("   argmax of CAM is at", tuple(int(v) for v in np.unravel_index(
        int(np.argmax(M)), M.shape)))

    print(SEP)
    print("3. with a bias the identity is logit - bias = mean(CAM)")
    b = 0.5
    print("   bias %.1f -> logit %.2f, mean(CAM) %.2f, logit-bias %.2f"
          % (b, y + b, M.mean(), y))

    print(SEP)
    print("4. identity check on a random net (K=6, H=W=7, C=4)")
    K, H, W, C = 6, 7, 7, 4
    Aa = rng.random((K, H, W))
    Wk = rng.normal(size=(C, K))
    gap = Aa.mean(axis=(1, 2))
    logits = Wk @ gap
    cam = np.einsum("ck,khw->chw", Wk, Aa)
    print("   logits:", np.round(logits, 4))
    print("   mean(CAM) per class:", np.round(cam.mean(axis=(1, 2)), 4))
    print("   max abs difference: %.2e"
          % float(np.abs(logits - cam.mean(axis=(1, 2))).max()))
    print("   CAM shape", cam.shape, "-> upsample to the input size for display")

    print(SEP)
    print("5. Grad-CAM on a pure GAP+Linear net")
    print("   d y_c / d A_k(x,y) = w[k,c] / (H*W)")
    grad = np.array([[Wk[c, k] / (H * W) for k in range(K)] for c in range(C)])
    alpha = grad.copy()                # spatial mean of a constant gradient
    print("   alpha (Grad-CAM weights) == w/(H*W)?  %s"
          % bool(np.allclose(alpha, Wk / (H * W))))
    c0 = 1
    gradcam = np.maximum((alpha[c0] * Aa.transpose(1, 2, 0)).sum(axis=2), 0)
    cam_scaled = cam[c0] / (H * W)
    print("   Grad-CAM map == ReLU(CAM / (H*W))?  %s"
          % bool(np.allclose(gradcam, np.maximum(cam_scaled, 0))))
    print("   max abs difference: %.2e"
          % float(np.abs(gradcam - np.maximum(cam_scaled, 0)).max()))

    print(SEP)
    print("6. why CAM needs GAP: flatten + FC has no per-map weight")
    hw = 7 * 7
    print("   GAP + Linear : %d weights, one per (channel, class)" % K)
    print("   Flatten + FC : %d weights, one per (pixel, channel, class)"
          % (K * hw * C))
    print("   ratio: %.0fx more weights, and none of them maps back to a single feature map"
          % ((K * hw * C) / float(K)))

    print(SEP)
    print("7. CAM resolution")
    for side, stride in ((224, 32), (128, 32), (32, 32)):
        c = side // stride
        print("   input %dx%d -> last conv %dx%d -> CAM %dx%d (upsample x%d to the input)"
              % (side, side, c, c, c, c, stride))
    print(SEP)


if __name__ == "__main__":
    main()
