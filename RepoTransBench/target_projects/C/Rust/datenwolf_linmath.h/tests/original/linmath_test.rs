// Translation of linmath_test.h, linmath_test.c, and all inline generated tests from original batch
use datenwolf_linmath::*;
use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;

const LINMATH_EPS: f32 = 0.0001;
fn linmath_is_close(val1: f32, val2: f32) -> bool {
    (val1 - val2).abs() < LINMATH_EPS
}

// Helper macros as functions
fn linmath_vec_set<const N: usize>(v: &mut [f32; N], value: f32) {
    for i in 0..N {
        v[i] = value;
    }
}

fn linmath_vec_init_random<const N: usize>(v: &mut [f32; N], seed: u64) {
    let mut rng = StdRng::seed_from_u64(seed);
    for x in v.iter_mut() {
        *x = rng.gen::<f32>();
    }
}

fn linmath_vec_allclose<const N: usize>(a: &[f32; N], b: &[f32; N]) -> bool {
    a.iter().zip(b.iter()).all(|(a, b)| linmath_is_close(*a, *b))
}

#[test]
fn test_vec2_mul_inner() {
    let mut v = [0.0; 2];
    linmath_vec_set(&mut v, 1.0);
    let inner_prod = vec2_mul_inner(v, v);
    assert!(linmath_is_close(inner_prod, 2.0));
}

#[test]
fn test_vec3_mul_inner() {
    let mut v = [0.0; 3];
    linmath_vec_set(&mut v, 1.0);
    let inner_prod = vec3_mul_inner(v, v);
    assert!(linmath_is_close(inner_prod, 3.0));
}

#[test]
fn test_vec4_mul_inner() {
    let mut v = [0.0; 4];
    linmath_vec_set(&mut v, 1.0);
    let inner_prod = vec4_mul_inner(v, v);
    assert!(linmath_is_close(inner_prod, 4.0));
}

#[test]
fn test_vec2_len() {
    let v = [1.0, 1.0];
    let norm = vec2_len(v);
    assert!(linmath_is_close(norm, f32::sqrt(2.0)));
}

#[test]
fn test_vec3_len() {
    let v = [1.0, 1.0, 1.0];
    let norm = vec3_len(v);
    assert!(linmath_is_close(norm, f32::sqrt(3.0)));
}

#[test]
fn test_vec4_len() {
    let v = [1.0, 1.0, 1.0, 1.0];
    let norm = vec4_len(v);
    assert!(linmath_is_close(norm, f32::sqrt(4.0)));
}

#[test]
fn test_vec2_norm() {
    let mut v = [0.0; 2];
    linmath_vec_init_random(&mut v, 17);
    let mut r = [0.0; 2];
    vec2_norm(&mut r, v);
    let norm = vec2_len(r);
    assert!(linmath_is_close(norm, 1.0));
}

#[test]
fn test_vec3_norm() {
    let mut v = [0.0; 3];
    linmath_vec_init_random(&mut v, 17);
    let mut r = [0.0; 3];
    vec3_norm(&mut r, v);
    let norm = vec3_len(r);
    assert!(linmath_is_close(norm, 1.0));
}

#[test]
fn test_vec4_norm() {
    let mut v = [0.0; 4];
    linmath_vec_init_random(&mut v, 17);
    let mut r = [0.0; 4];
    vec4_norm(&mut r, v);
    let norm = vec4_len(r);
    assert!(linmath_is_close(norm, 1.0));
}

#[test]
fn test_vec3_mul_cross() {
    let mut v1 = [0.0; 3];
    linmath_vec_init_random(&mut v1, 13);
    let mut v2 = v1;
    let mut r = [0.0; 3];
    vec3_mul_cross(&mut r, v1, v2);
    let v_expected = [0.0, 0.0, 0.0];
    assert!(linmath_vec_allclose(&r, &v_expected));

    // test ijk axes
    let i = [1.0, 0.0, 0.0];
    let j = [0.0, 1.0, 0.0];
    let k = [0.0, 0.0, 1.0];
    vec3_mul_cross(&mut r, i, j);
    assert!(linmath_vec_allclose(&r, &k));
}

#[test]
fn test_vec4_mul_cross() {
    let mut v1 = [0.0; 4];
    linmath_vec_init_random(&mut v1, 13);
    let mut v2 = v1;
    let mut r = [0.0; 4];
    vec4_mul_cross(&mut r, v1, v2);
    let mut v_expected = [0.0; 4];
    v_expected[3] = 1.0;
    assert!(linmath_vec_allclose(&r, &v_expected));

    let i = [1.0, 0.0, 0.0, 1.0];
    let j = [0.0, 1.0, 0.0, 1.0];
    let k = [0.0, 0.0, 1.0, 1.0];
    vec4_mul_cross(&mut r, i, j);
    assert!(linmath_vec_allclose(&r, &k));
}

fn linmath_mat4x4_allclose(m: &Mat4x4, n: &Mat4x4) -> bool {
    (0..4).all(|i| linmath_vec_allclose(&m[i], &n[i]))
}

#[test]
fn test_quat_rotate() {
    let axis = [0.0, 1.0, 0.0];
    let mut q = [0.0; 4];
    let theta = std::f32::consts::FRAC_PI_4;
    quat_rotate(&mut q, theta, axis);
    let q_reference = [0.0, f32::sin(theta/2.0), 0.0, f32::cos(theta/2.0)];
    assert!(linmath_vec_allclose(&q, &q_reference));
}

#[test]
fn test_quat_conj() {
    let mut rng = StdRng::seed_from_u64(15);
    let mut q = [0.0; 4];
    let axis = [0.0, 1.0, 0.0];
    let angle_rads = rng.gen::<f32>();
    quat_rotate(&mut q, angle_rads, axis);
    let mut q_conj = [0.0; 4];
    quat_conj(&mut q_conj, q);
    let mut q_reference = [0.0; 4];
    quat_rotate(&mut q_reference, -angle_rads, axis);
    assert!(linmath_vec_allclose(&q_conj, &q_reference));
}

#[test]
fn test_quat_mul_vec3() {
    let mut rng = StdRng::seed_from_u64(11);
    let mut q = [0.0; 4];
    let axis = [0.0, 1.0, 0.0];
    let angle_rads = rng.gen::<f32>();
    quat_rotate(&mut q, angle_rads, axis);
    let mut q_conj = [0.0; 4];
    quat_conj(&mut q_conj, q);

    let mut v_initial = [0.0; 3];
    linmath_vec_init_random(&mut v_initial, 11);
    let mut v_rotated = [0.0; 3];
    let mut v_restored = [0.0; 3];
    quat_mul_vec3(&mut v_rotated, q, v_initial);
    quat_mul_vec3(&mut v_restored, q_conj, v_rotated);
    assert!(linmath_vec_allclose(&v_restored, &v_initial));
}

#[test]
fn test_mat4x4o_mul_quat() {
    let mut rng = StdRng::seed_from_u64(12);
    let mut q = [0.0; 4];
    let axis = [0.0, 1.0, 0.0];
    let angle_rads = rng.gen::<f32>();
    quat_rotate(&mut q, angle_rads, axis);
    let mut q_conj = [0.0; 4];
    quat_conj(&mut q_conj, q);

    let mut m_reference = [[0.0; 4]; 4];
    mat4x4_identity(&mut m_reference);
    m_reference[0][3] = 0.1;
    m_reference[1][3] = 0.2;
    m_reference[2][3] = 0.3;
    let mut m_rotated = [[0.0; 4]; 4];
    mat4x4o_mul_quat(&mut m_rotated, m_reference, q);
    let mut m = [[0.0; 4]; 4];
    mat4x4o_mul_quat(&mut m, m_rotated, q_conj);
    assert!(linmath_mat4x4_allclose(&m_reference, &m));
}

//
// linmath_test_extra.c translations below
//
fn allclose(a: f32, b: f32, eps: f32) -> bool {
    (a - b).abs() <= eps
}

#[test]
fn test_vec2_minmax_dup() {
    let a = [1.0f32, -2.0f32];
    let b = [0.5, 3.2];
    let mut r = [0.0, 0.0];
    let expect_min = [0.5, -2.0];
    let expect_max = [1.0, 3.2];
    let mut out = [0.0, 0.0];

    vec2_min(&mut r, a, b);
    assert!(allclose(r[0], expect_min[0], 1e-6));
    assert!(allclose(r[1], expect_min[1], 1e-6));

    vec2_max(&mut r, a, b);
    assert!(allclose(r[0], expect_max[0], 1e-6));
    assert!(allclose(r[1], expect_max[1], 1e-6));

    vec2_dup(&mut out, a);
    assert!(allclose(out[0], a[0], 1e-6));
    assert!(allclose(out[1], a[1], 1e-6));
}

#[test]
fn test_vec3_functions() {
    let a = [1.0, 0.0, -1.0];
    let b = [2.5, -3.0, 0.0];
    let mut r = [0.0; 3];

    // Cross
    vec3_mul_cross(&mut r, a, b);
    assert!(allclose(r[0], -3.0, 1e-6));
    assert!(allclose(r[1], -2.5, 1e-6));
    assert!(allclose(r[2], -3.0, 1e-6));

    // Reflect - normal axis aligned
    let v = [1.0, -2.0, 0.5];
    let n = [0.0, 1.0, 0.0];
    let expect_reflect = [1.0, 2.0, 0.5];
    vec3_reflect(&mut r, v, n);
    assert!(allclose(r[0], expect_reflect[0], 1e-6));
    assert!(allclose(r[1], expect_reflect[1], 1e-6));
    assert!(allclose(r[2], expect_reflect[2], 1e-6));
}

#[test]
fn test_vec4_functions() {
    let a = [2.0, 3.0, -1.0, 0.0];
    let b = [0.0, 1.0, 4.0, 2.0];
    let mut r = [0.0; 4];

    // Cross product for vec4
    let expect_cross = [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0],
        1.0
    ];
    vec4_mul_cross(&mut r, a, b);
    assert!(allclose(r[0], expect_cross[0], 1e-6));
    assert!(allclose(r[1], expect_cross[1], 1e-6));
    assert!(allclose(r[2], expect_cross[2], 1e-6));
    assert!(allclose(r[3], expect_cross[3], 1e-6));

    // Reflect
    let v = [1.0, 2.0, -1.0, 1.5];
    let n = [0.0, 1.0, 0.0, 0.0];
    let expect_reflect = [1.0, -2.0, -1.0, 1.5];
    vec4_reflect(&mut r, v, n);
    assert!(allclose(r[0], expect_reflect[0], 1e-6));
    assert!(allclose(r[1], expect_reflect[1], 1e-6));
    assert!(allclose(r[2], expect_reflect[2], 1e-6));
    assert!(allclose(r[3], expect_reflect[3], 1e-6));
}