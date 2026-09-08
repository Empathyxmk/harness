import numpy as np
import math
from src.linmath import *

def ALLCLOSE(a, b, eps):
    return abs(a - b) <= eps

def test_vec2_minmax_dup():
    a = np.array([1.0, -2.0], dtype=np.float32)
    b = np.array([0.5, 3.2], dtype=np.float32)
    r = np.zeros(2, dtype=np.float32)
    expect_min = np.array([0.5, -2.0], dtype=np.float32)
    expect_max = np.array([1.0, 3.2], dtype=np.float32)
    out = np.empty(2, dtype=np.float32)
    vec2_min(r, a, b)
    assert ALLCLOSE(r[0], expect_min[0], 1e-6)
    assert ALLCLOSE(r[1], expect_min[1], 1e-6)
    vec2_max(r, a, b)
    assert ALLCLOSE(r[0], expect_max[0], 1e-6)
    assert ALLCLOSE(r[1], expect_max[1], 1e-6)
    vec2_dup(out, a)
    assert ALLCLOSE(out[0], a[0], 1e-6)
    assert ALLCLOSE(out[1], a[1], 1e-6)

def test_vec3_functions():
    a = np.array([1.0, 0.0, -1.0], dtype=np.float32)
    b = np.array([2.5, -3.0, 0.0], dtype=np.float32)
    r = np.empty(3, dtype=np.float32)
    # Cross product
    vec3_mul_cross(r, a, b)
    assert ALLCLOSE(r[0], -3.0, 1e-6)
    assert ALLCLOSE(r[1], -2.5, 1e-6)
    assert ALLCLOSE(r[2], -3.0, 1e-6)
    # Reflect
    v = np.array([1.0, -2.0, 0.5], dtype=np.float32)
    n = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    expect_reflect = np.array([1.0, 2.0, 0.5], dtype=np.float32)
    vec3_reflect(r, v, n)
    assert ALLCLOSE(r[0], expect_reflect[0], 1e-6)
    assert ALLCLOSE(r[1], expect_reflect[1], 1e-6)
    assert ALLCLOSE(r[2], expect_reflect[2], 1e-6)

def test_vec4_functions():
    a = np.array([2.0, 3.0, -1.0, 0.0], dtype=np.float32)
    b = np.array([0.0, 1.0, 4.0, 2.0], dtype=np.float32)
    r = np.empty(4, dtype=np.float32)
    # Cross
    expect_cross = np.zeros(4, dtype=np.float32)
    expect_cross[0] = a[1]*b[2] - a[2]*b[1]   # 3*4 - (-1)*1 = 12 + 1 = 13
    expect_cross[1] = a[2]*b[0] - a[0]*b[2]   # -1*0 - 2*4 = 0 - 8 = -8
    expect_cross[2] = a[0]*b[1] - a[1]*b[0]   # 2*1 - 3*0 = 2 - 0 = 2
    expect_cross[3] = 1.0
    vec4_mul_cross(r, a, b)
    assert ALLCLOSE(r[0], expect_cross[0], 1e-6)
    assert ALLCLOSE(r[1], expect_cross[1], 1e-6)
    assert ALLCLOSE(r[2], expect_cross[2], 1e-6)
    assert ALLCLOSE(r[3], expect_cross[3], 1e-6)
    # Reflect
    v = np.array([1.0, 2.0, -1.0, 1.5], dtype=np.float32)
    n = np.array([0.0, 1.0, 0.0, 0.0], dtype=np.float32)
    expect_reflect = np.array([1.0, -2.0, -1.0, 1.5], dtype=np.float32)
    vec4_reflect(r, v, n)
    assert ALLCLOSE(r[0], expect_reflect[0], 1e-6)
    assert ALLCLOSE(r[1], expect_reflect[1], 1e-6)
    assert ALLCLOSE(r[2], expect_reflect[2], 1e-6)
    assert ALLCLOSE(r[3], expect_reflect[3], 1e-6)