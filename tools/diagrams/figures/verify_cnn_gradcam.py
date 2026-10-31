# -*- coding: utf-8 -*-
"""Numbers for the Grad-CAM page.

    python verify_cnn_gradcam.py
"""
import numpy as np

SEP = "-" * 72
rng = np.random.default_rng(31)


def main():
    A = [np.array([[10.0, 0.0], [8.0, 2.0]]),
         np.array([[1.0, 1.0], [1.0, 1.0]]),
         np.array([[0.0, 2.0], [0.0, 2.0]])]
    grad = [np.array([[0.2, 0.4], [0.1, 0.3]]),
            np.array([[0.1, 0.1], [0.1, 0.1]]),
            np.array([[-0.2, -0.2], [-0.2, -0.2]])]

    print(SEP)
    print("1. step 4: average the gradient of each map -> alpha")
    alpha = []
    for k, g in enumerate(grad, start=1):
        a = float(g.mean())
        alpha.append(a)
        print("   d y / d A%d = %s   ->  alpha%d = %.4f"
              % (k, g.tolist(), k, a))
    alpha = np.array(alpha)

    print(SEP)
    print("2. step 5-6: weighted sum, then ReLU")
    L = sum(a * m for a, m in zip(alpha, A))
    print("   L = 0.25*A1 + 0.1*A2 - 0.2*A3 =\n", np.round(L, 3))
    print("   ReLU(L) =\n", np.round(np.maximum(L, 0), 3))
    print("   cells removed by ReLU: %d of %d"
          % (int((L < 0).sum()), L.size))

    print(SEP)
    print("3. same maps, CAM weights instead of gradients (page 7)")
    w = np.array([0.8, 0.1, -0.2])
    cam = sum(wk * m for wk, m in zip(w, A))
    print("   CAM  = 0.8*A1 + 0.1*A2 - 0.2*A3 =\n", np.round(cam, 3))
    print("   mean(CAM) = %.3f   (the class logit, from page 7)" % cam.mean())
    print("   CAM vs Grad-CAM differ because alpha != w:",
          np.round(alpha, 3).tolist(), "vs", w.tolist())

    print(SEP)
    print("4. the gradient is not always w: put a ReLU before the GAP")
    K, H, W = 3, 4, 4
    Aa = rng.normal(size=(K, H, W))
    ww = np.array([1.5, -0.7, 0.4])
    X = np.maximum(Aa, 0)
    y = float((ww * X.mean(axis=(1, 2))).sum())
    analytic = ww[:, None, None] / (H * W) * (Aa > 0)
    print("   model: A -> ReLU -> GAP -> Linear,  y = %.4f" % y)

    def f(Ain):
        return float((ww * np.maximum(Ain, 0).mean(axis=(1, 2))).sum())

    eps = 1e-6
    fd = np.zeros_like(Aa)
    for idx in np.ndindex(Aa.shape):
        e = np.zeros_like(Aa)
        e[idx] = eps
        fd[idx] = (f(Aa + e) - f(Aa - e)) / (2 * eps)
    print("   analytic vs finite difference: %s (max diff %.2e)"
          % (bool(np.allclose(analytic, fd, atol=1e-6)),
             float(np.abs(analytic - fd).max())))
    print("   alpha = mean gradient =", np.round(analytic.mean(axis=(1, 2)), 4))
    print("   w / (H*W)             =", np.round(ww / (H * W), 4))
    print("   -> equal only where ReLU passes everything")

    print(SEP)
    print("5. pure GAP + Linear: Grad-CAM collapses onto CAM")
    Aa = rng.random((5, 7, 7))
    Wk = rng.normal(size=(3, 5))
    gap = Aa.mean(axis=(1, 2))
    logits = Wk @ gap
    cam = np.einsum("ck,khw->chw", Wk, Aa)
    alpha2 = Wk / (7 * 7)
    gradcam = np.maximum(np.einsum("ck,khw->chw", alpha2, Aa), 0)
    print("   logits:", np.round(logits, 4))
    print("   mean(CAM) by class:", np.round(cam.mean(axis=(1, 2)), 4))
    print("   identity max abs diff: %.2e"
          % float(np.abs(logits - cam.mean(axis=(1, 2))).max()))
    print("   Grad-CAM == ReLU(CAM/(H*W))? %s (max diff %.2e)"
          % (bool(np.allclose(gradcam, np.maximum(cam / (7 * 7), 0))),
             float(np.abs(gradcam - np.maximum(cam / (7 * 7), 0)).max())))

    print(SEP)
    print("6. what the upsample does")
    print("   7x7 = 49 values -> bilinear to 224x224 = 50,176 pixels (x32 each side)")
    print("   scaling: min-max to 0-1, then a colormap; no new information is created")

    print(SEP)
    print("7. picking a layer: replay the same idea at three depths")
    for name, side, ch in (("early", 56, 64), ("mid", 28, 128), ("last", 7, 512)):
        print("   %-5s conv %2dx%2dx%-3d -> heat map %2dx%2d, upsample x%d"
              % (name, side, side, ch, side, side, 224 // side))
    print(SEP)


if __name__ == "__main__":
    main()
