import numpy as np
import math
import random
from src.linmath import *

LINMATH_EPS = 0.0001

def linmath_is_close(val1, val2):
    return abs(val1 - val2) < LINMATH_EPS

def linmath_vec2_set(v, value):
    v[:] = value

def linmath_vec3_set(v, value):
    v[:] = value

def linmath_vec4_set(v, value):
    v[:] = value

def linmath_vec2_init_random(v):
    np.random.seed(11)
    v[:] = np.random.rand(2)

def linmath_vec3_init_random(v):
    np.random.seed(13)
    v[:] = np.random.rand(3)

def linmath_vec4_init_random(v):
    np.random.seed(14)
    v[:] = np.random.rand(4)

def linmath_vec2_allclose(a, b):
    return all(linmath_is_close(a[i], b[i]) for i in range(2))

def linmath_vec3_allclose(a, b):
    return all(linmath_is_close(a[i], b[i]) for i in range(3))

def linmath_vec4_allclose(a, b):
    return all(linmath_is_close(a[i], b[i]) for i in range(4))

def linmath_mat4x4_allclose(m1, m2):
    return all(linmath_vec4_allclose(m1[i], m2[i]) for i in range(4))

def test_vec2_mul_inner():
    v = np.ones(2, dtype=np.float32)
    inner_prod = vec2_mul_inner(v, v)
    assert linmath_is_close(inner_prod, 2)

def test_vec3_mul_inner():
    v = np.ones(3, dtype=np.float32)
    inner_prod = vec3_mul_inner(v, v)
    assert linmath_is_close(inner_prod, 3)

def test_vec4_mul_inner():
    v = np.ones(4, dtype=np.float32)
    inner_prod = vec4_mul_inner(v, v)
    assert linmath_is_close(inner_prod, 4)

def test_vec2_len():
    v = np.ones(2, dtype=np.float32)
    norm = vec2_len(v)
    assert linmath_is_close(norm, math.sqrt(2))

def test_vec3_len():
    v = np.ones(3, dtype=np.float32)
    norm = vec3_len(v)
    assert linmath_is_close(norm, math.sqrt(3))

def test_vec4_len():
    v = np.ones(4, dtype=np.float32)
    norm = vec4_len(v)
    assert linmath_is_close(norm, math.sqrt(4))

def test_vec2_norm():
    np.random.seed(17)
    v = np.random.rand(2).astype(np.float32)
    r = np.empty_like(v)
    vec2_norm(r, v)
    norm = vec2_len(r)
    assert linmath_is_close(norm, 1.0)

def test_vec3_norm():
    np.random.seed(17)
    v = np.random.rand(3).astype(np.float32)
    r = np.empty_like(v)
    vec3_norm(r, v)
    norm = vec3_len(r)
    assert linmath_is_close(norm, 1.0)

def test_vec4_norm():
    np.random.seed(17)
    v = np.random.rand(4).astype(np.float32)
    r = np.empty_like(v)
    vec4_norm(r, v)
    norm = vec4_len(r)
    assert linmath_is_close(norm, 1.0)

def test_vec3_mul_cross():
    np.random.seed(13)
    v1 = np.random.rand(3).astype(np.float32)
    v2 = v1.copy()
    r = np.empty_like(v1)
    vec3_mul_cross(r, v1, v2)
    v_expected = np.zeros(3, dtype=np.float32)
    assert linmath_vec3_allclose(r, v_expected)
    # test ijk axes
    i = np.array([1,0,0], dtype=np.float32)
    j = np.array([0,1,0], dtype=np.float32)
    k = np.array([0,0,1], dtype=np.float32)
    vec3_mul_cross(r, i, j)
    assert linmath_vec3_allclose(r, k)

def test_vec4_mul_cross():
    np.random.seed(13)
    v1 = np.random.rand(4).astype(np.float32)
    v2 = v1.copy()
    r = np.empty_like(v1)
    vec4_mul_cross(r, v1, v2)
    v_expected = np.zeros(4, dtype=np.float32)
    v_expected[3] = 1.0
    assert linmath_vec4_allclose(r, v_expected)
    # test ijk axes
    i = np.array([1,0,0,1], dtype=np.float32)
    j = np.array([0,1,0,1], dtype=np.float32)
    k = np.array([0,0,1,1], dtype=np.float32)
    vec4_mul_cross(r, i, j)
    assert linmath_vec4_allclose(r, k)

def test_quat_rotate():
    axis = np.array([0,1,0], dtype=np.float32)
    theta = 0.7853981633974483
    q = np.zeros(4, dtype=np.float32)
    quat_rotate(q, theta, axis)
    q_reference = np.array([0, math.sin(theta/2), 0, math.cos(theta/2)], dtype=np.float32)
    assert linmath_vec4_allclose(q, q_reference)

def test_quat_conj():
    np.random.seed(15)
    axis = np.array([0,1,0], dtype=np.float32)
    angle_rads = np.random.rand(1).astype(np.float32)[0]
    q = np.zeros(4, dtype=np.float32)
    quat_rotate(q, angle_rads, axis)
    q_conj = np.empty(4, dtype=np.float32)
    quat_conj(q_conj, q)
    q_reference = np.zeros(4, dtype=np.float32)
    quat_rotate(q_reference, -angle_rads, axis)
    assert linmath_vec4_allclose(q_conj, q_reference)

def test_quat_mul_vec3():
    np.random.seed(11)
    axis = np.array([0,1,0], dtype=np.float32)
    angle_rads = np.random.rand(1).astype(np.float32)[0]
    q = np.zeros(4, dtype=np.float32)
    quat_rotate(q, angle_rads, axis)
    q_conj = np.empty(4, dtype=np.float32)
    quat_conj(q_conj, q)
    v_initial = np.random.rand(3).astype(np.float32)
    v_rotated = np.empty(3, dtype=np.float32)
    quat_mul_vec3(v_rotated, q, v_initial)
    v_restored = np.empty(3, dtype=np.float32)
    quat_mul_vec3(v_restored, q_conj, v_rotated)
    assert linmath_vec3_allclose(v_restored, v_initial)

def test_mat4x4o_mul_quat():
    np.random.seed(12)
    axis = np.array([0,1,0], dtype=np.float32)
    angle_rads = np.random.rand(1).astype(np.float32)[0]
    q = np.zeros(4, dtype=np.float32)
    quat_rotate(q, angle_rads, axis)
    q_conj = np.empty(4, dtype=np.float32)
    quat_conj(q_conj, q)
    m_reference = np.eye(4, dtype=np.float32)
    m_reference[0,3] = 0.1
    m_reference[1,3] = 0.2
    m_reference[2,3] = 0.3
    m_rotated = np.empty((4,4), dtype=np.float32)
    mat4x4o_mul_quat(m_rotated, m_reference, q)
    m = np.empty((4,4), dtype=np.float32)
    mat4x4o_mul_quat(m, m_rotated, q_conj)
    assert linmath_mat4x4_allclose(m_reference, m)

# The following functional is commented out in C test too:
# def test_quat_from_mat4x4():
#     np.random.seed(7)
#     axis = np.array([0,1,0], dtype=np.float32)
#     angle_rads = np.random.rand(1).astype(np.float32)[0]
#     q_reference = np.zeros(4, dtype=np.float32)
#     quat_rotate(q_reference, angle_rads, axis)
#     m_identity = np.eye(4, dtype=np.float32)
#     m_rotated = np.empty((4,4), dtype=np.float32)
#     mat4x4o_mul_quat(m_rotated, m_identity, q_reference)
#     q_restored = np.empty(4, dtype=np.float32)
#     quat_from_mat4x4(q_restored, m_rotated)
#     assert linmath_vec4_allclose(q_restored, q_reference)