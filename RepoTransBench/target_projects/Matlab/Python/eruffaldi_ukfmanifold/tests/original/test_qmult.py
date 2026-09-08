import numpy as np
from ukfmanifold.quaternions import qmult, qnorm

def test_multiplicative_identity():
    I = np.array([0,0,0,1.0])
    q = np.array([0.5, -0.3, 0.2, 0.7])
    out = qmult(q, I)
    assert np.allclose(out, q, atol=1e-12)
    out2 = qmult(I, q)
    assert np.allclose(out2, q, atol=1e-12)

def test_random_products_are_normed():
    Q1 = np.random.randn(10, 4)
    Q2 = np.random.randn(10, 4)
    Q1 = np.array([qnorm(q) for q in Q1])
    Q2 = np.array([qnorm(q) for q in Q2])
    outs = np.array([qmult(q1, q2) for q1, q2 in zip(Q1, Q2)])
    for q in outs:
        assert np.isclose(np.linalg.norm(q), 1.0, rtol=1e-10)