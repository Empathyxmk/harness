import numpy as np
import math
from src.linmath import *

PUB_EPS = 0.0002

def pub_is_close(val1, val2):
    return abs(val1 - val2) < PUB_EPS

def pub_vec2_set(v, value):
    v[:] = value

def pub_vec3_set(v, value):
    v[:] = value

def pub_vec4_set(v, value):
    v[:] = value

def pub_vec2_init_fixed(v):
    v[0] = 0.2
    v[1] = 3.4

def pub_vec3_init_fixed(v):
    v[0] = -1.0
    v[1] = 2.5
    v[2] = 0.75

def pub_vec4_init_fixed(v):
    v[0] = 2.1
    v[1] = 1.9
    v[2] = -3.2
    v[3] = 0.0

def pub_vec2_allclose(a, b):
    return pub_is_close(a[0], b[0]) and pub_is_close(a[1], b[1])

def pub_vec3_allclose(a, b):
    return pub_is_close(a[0], b[0]) and pub_is_close(a[1], b[1]) and pub_is_close(a[2], b[2])

def pub_vec4_allclose(a, b):
    return (pub_is_close(a[0], b[0])
            and pub_is_close(a[1], b[1])
            and pub_is_close(a[2], b[2])
            and pub_is_close(a[3], b[3]))

def test_pub_vec2_mul_inner():
    v = np.array([2.5, 2.5], dtype=np.float32)
    inner = vec2_mul_inner(v, v)
    assert pub_is_close(inner, 2 * (2.5 * 2.5))

def test_pub_vec3_mul_inner():
    v = np.array([-3.0, 1.0, 2.0], dtype=np.float32)
    inner = vec3_mul_inner(v, v)
    assert pub_is_close(inner, 9.0 + 1.0 + 4.0)

def test_pub_vec4_mul_inner():
    v = np.array([0.0, 0.5, -1.5, 3.5], dtype=np.float32)
    inner = vec4_mul_inner(v, v)
    assert pub_is_close(inner, 0.0*0.0 + 0.5*0.5 + 1.5*1.5 + 3.5*3.5)

def test_pub_vec2_len():
    v = np.array([6.0, 8.0], dtype=np.float32)
    norm = vec2_len(v)
    assert pub_is_close(norm, 10.0)

def test_pub_vec3_len():
    v = np.array([1.0, 2.0, 2.0], dtype=np.float32)
    norm = vec3_len(v)
    assert pub_is_close(norm, 3.0)

def test_pub_vec4_len():
    v = np.array([1.0, 2.0, 2.0, 3.0], dtype=np.float32)
    norm = vec4_len(v)
    assert pub_is_close(norm, math.sqrt(1.0 + 4.0 + 4.0 + 9.0))

def test_pub_vec2_norm():
    v = np.array([3.0, 4.0], dtype=np.float32)
    r = np.empty(2, dtype=np.float32)
    vec2_norm(r, v)
    norm = vec2_len(r)
    assert pub_is_close(norm, 1.0)

def test_pub_vec3_norm():
    v = np.array([10.0, 0.0, 5.0], dtype=np.float32)
    r = np.empty(3, dtype=np.float32)
    vec3_norm(r, v)
    norm = vec3_len(r)
    assert pub_is_close(norm, 1.0)

def test_pub_vec4_norm():
    v = np.array([-2.0, 0.0, 0.0, 0.0], dtype=np.float32)
    r = np.empty(4, dtype=np.float32)
    vec4_norm(r, v)
    norm = vec4_len(r)
    assert pub_is_close(norm, 1.0)

def test_pub_vec3_mul_cross():
    a = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    b = np.array([0.0, 0.0, 2.0], dtype=np.float32)
    r = np.empty(3, dtype=np.float32)
    vec3_mul_cross(r, a, b)
    assert pub_is_close(r[0], 0.0) and pub_is_close(r[1], -2.0) and pub_is_close(r[2], 0.0)

def test_pub_vec3_reflect():
    v = np.array([3.0, -2.0, 5.0], dtype=np.float32)
    n = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    r = np.empty(3, dtype=np.float32)
    vec3_reflect(r, v, n)
    assert pub_is_close(r[0], 3.0) and pub_is_close(r[1], 2.0) and pub_is_close(r[2], 5.0)