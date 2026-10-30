# -*- coding: utf-8 -*-
"""Every number on the 全連接層 page is computed here first.

    python verify_cnn_fully_connected.py
"""
import numpy as np

SEP = "-" * 72
rng = np.random.default_rng(11)


def softmax(z):
    e = np.exp(z - np.max(z))
    return e / e.sum()


def main():
    x = np.array([2.0, 1.0, 0.0, 3.0])
    W = np.array([[0.2, 0.4, -0.1, 0.5],
                  [0.7, -0.3, 0.2, 0.1],
                  [-0.5, 0.6, 0.8, -0.2]])
    b = np.array([0.1, -0.2, 0.3])

    print(SEP)
    print("1. z = Wx + b   (4 in, 3 out)")
    print("   x:", x, " W.shape:", W.shape, " b:", b)
    d = (W * x).sum(axis=1)
    print("   row-by-row dot product, before bias:", d)
    z = W @ x + b
    print("   z = Wx + b :", np.round(z, 4))
    print("   step by step:")
    for j in range(3):
        terms = " + ".join("%.1f×%.0f" % (W[j, i], x[i]) for i in range(4))
        print("     z%d = (%s) + %.1f = %.4f" % (j + 1, terms, b[j], z[j]))

    print(SEP)
    print("2. what the draft's numbers would require")
    print("   draft claims z = [2.4, 1.5, 1.1]")
    print("   computed     z =", np.round(z, 4))
    print("   difference   :", np.round(np.array([2.4, 1.5, 1.1]) - z, 4))

    print(SEP)
    print("3. softmax")
    for name, v in (("computed z", z), ("draft z [2.4, 1.5, 1.1]", np.array([2.4, 1.5, 1.1]))):
        p = softmax(v)
        print("   %-24s -> %s  sum = %.6f" % (name, np.round(p, 4), p.sum()))
    print("   draft claims [0.55, 0.22, 0.15], which sums to",
          round(0.55 + 0.22 + 0.15, 2))

    print(SEP)
    print("4. softmax properties")
    p = softmax(z)
    print("   shift all logits by +100 -> same probabilities?",
          bool(np.allclose(softmax(z + 100), p)))
    print("   order preserved? argmax", int(np.argmax(z)), "==", int(np.argmax(p)))
    print("   max-minus-min of logits: %.2f -> probability ratio %.2f"
          % (z.max() - z.min(), p.max() / p.min()))

    print(SEP)
    print("5. parameter counts   params = m*n + m")
    for n_in, n_out in ((3136, 128), (3136, 10), (784, 64), (64, 10), (128, 10)):
        print("   %4d -> %3d : %d weights + %d bias = %d"
              % (n_in, n_out, n_in * n_out, n_out, n_in * n_out + n_out))
    conv = 3 * 3 * 1 * 8 + 8 + 3 * 3 * 8 * 16 + 16
    fc = 784 * 64 + 64 + 64 * 10 + 10
    print("   small MNIST CNN: conv total %d, fc total %d -> fc is %.1f%% of %d"
          % (conv, fc, 100.0 * fc / (conv + fc), conv + fc))

    print(SEP)
    print("6. flatten does not compute anything")
    print("   7x7x64 = %d values; 7*7*64 = %d" % (7 * 7 * 64, 7 * 7 * 64))
    print("   7x7x64 -> 3136, params 0; the same numbers, new shape")

    print(SEP)
    print("7. backward pass of a fully connected layer")
    Wt = rng.normal(size=(5, 4))
    xt = rng.normal(size=4)
    delta = np.array([1.0, -0.5, 0.25, 0.0, 2.0])   # dL/dz
    grad_W = np.outer(delta, xt)
    print("   dL/dW = delta x^T, shape", grad_W.shape)
    print("   dL/dx = W^T delta, shape", (Wt.T @ delta).shape)
    # finite difference on one loss L = delta . (Wx)
    def loss(Wv):
        return float(delta @ (Wv @ xt))
    eps = 1e-6
    fd = np.zeros_like(Wt)
    for idx in np.ndindex(Wt.shape):
        e = np.zeros_like(Wt)
        e[idx] = eps
        fd[idx] = (loss(Wt + e) - loss(Wt - e)) / (2 * eps)
    print("   finite-difference matches delta x^T:", bool(np.allclose(fd, grad_W)))

    print(SEP)
    print("8. bias shifts every logit by the same amount")
    print("   z (bias 0) :", np.round((W @ x), 4))
    print("   z (bias+1) :", np.round((W @ x) + 1, 4))
    print("   softmax(bias 0) :", np.round(softmax(W @ x), 4))
    print("   softmax(bias+1) :", np.round(softmax((W @ x) + 1), 4))
    print(SEP)


if __name__ == "__main__":
    main()
