# -*- coding: utf-8 -*-
"""Numbers for the CAM vs Grad-CAM comparison page.

    python verify_cnn_cam_vs_gradcam.py
"""
import numpy as np

SEP = "-" * 72
rng = np.random.default_rng(41)


def main():
    print(SEP)
    print("1. same formula, different weight")
    print("   CAM      : L = ReLU( sum_k w[k,c]  * A_k )     w  = trained weights")
    print("   Grad-CAM : L = ReLU( sum_k a[k,c]  * A_k )     a  = mean of gradients")
    print("   the only difference is how the K numbers are obtained")

    print(SEP)
    print("2. a pure GAP+Linear model: alpha does NOT depend on the image")
    K, H, W, C = 3, 4, 4, 2
    Wk = np.array([[1.2, -0.5, 0.8], [-0.7, 0.9, 0.3]])   # (C, K)
    print("   classifier weights w (fixed, learned once):")
    print("     dog :", Wk[0], "   cat :", Wk[1])
    print("   d y_c / d A_k(i,j) = w[k,c] / (H*W) for every cell")
    print("     alpha(dog) =", np.round(Wk[0] / (H * W), 4),
          "  <- same for image A and image B")
    Aa = rng.random((K, H, W))
    Ab = rng.random((K, H, W))
    print("   image A is different from image B:",
          bool(not np.allclose(Aa, Ab)))
    print("   but alpha is identical for both (pure GAP+Linear).")

    print(SEP)
    print("3. put a ReLU before the GAP -> alpha becomes image-specific")
    print("   d y_c / d A_k(i,j) = w[k,c]/(H*W) * 1[A_k(i,j) > 0]")
    Aa = rng.normal(size=(K, H, W))
    Ab = rng.normal(size=(K, H, W))
    for name, A in (("image A", Aa), ("image B", Ab)):
        share = (A > 0).mean(axis=(1, 2))
        alpha = Wk[0] / (H * W) * share
        print("   %s: positive share per channel %s -> alpha(dog) %s"
              % (name, np.round(share, 2), np.round(alpha, 4)))
    print("   w/(H*W) claimed by the pure model:", np.round(Wk[0] / (H * W), 4))

    print(SEP)
    print("4. the #37 example from the page")
    idx = 37
    print("   feature map #%d of a 512-channel layer" % idx)
    print("   CAM      : w[%d, dog] = 0.80  (a stored parameter, same for every image)"
          % idx)
    print("   Grad-CAM : alpha[%d, dog] = 0.90 on this image, 0.60 on another, 1.20 on a third"
          % idx)

    print(SEP)
    print("5. what each method can explain (architecture checklist)")
    checks = [("Conv -> GAP -> Linear", "yes", "yes"),
              ("Conv -> Flatten -> FC", "no", "yes"),
              ("Conv -> 1x1 conv -> GAP -> Linear", "no", "yes"),
              ("ResNet / DenseNet with a linear head", "partly (needs the GAP head)", "yes")]
    print("   %-38s %-22s %s" % ("architecture", "CAM", "Grad-CAM"))
    for arch, cam, gc in checks:
        print("   %-38s %-22s %s" % (arch, cam, gc))

    print(SEP)
    print("6. cost per explanation")
    print("   CAM      : 1 forward, then a matrix lookup      (no backward pass)")
    print("   Grad-CAM : 1 forward + 1 backward per class")
    for classes in (1, 1000):
        print("   Grad-CAM over %4d classes: %4d backward passes" % (classes, classes))
    print(SEP)


if __name__ == "__main__":
    main()
