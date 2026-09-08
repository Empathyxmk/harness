// Translation of linmath_test_public.c to Rust
use datenwolf_linmath::*;

const PUB_EPS: f32 = 0.0002;
fn pub_is_close(val1: f32, val2: f32) -> bool {
    (val1 - val2).abs() < PUB_EPS
}

fn pub_vec2_set(v: &mut [f32; 2], value: f32) {
    v[0] = value;
    v[1] = value;
}
fn pub_vec3_set(v: &mut [f32; 3], value: f32) {
    v[0] = value;
    v[1] = value;
    v[2] = value;
}
fn pub_vec4_set(v: &mut [f32; 4], value: f32) {
    v[0] = value;
    v[1] = value;
    v[2] = value;
    v[3] = value;
}
fn pub_vec2_init_fixed(v: &mut [f32; 2]) {
    v[0] = 0.2;
    v[1] = 3.4;
}
fn pub_vec3_init_fixed(v: &mut [f32; 3]) {
    v[0] = -1.0;
    v[1] = 2.5;
    v[2] = 0.75;
}
fn pub_vec4_init_fixed(v: &mut [f32; 4]) {
    v[0] = 2.1;
    v[1] = 1.9;
    v[2] = -3.2;
    v[3] = 0.0;
}
fn pub_vec2_allclose(a: &[f32;2], b: &[f32;2]) -> bool {
    pub_is_close(a[0], b[0]) && pub_is_close(a[1], b[1])
}
fn pub_vec3_allclose(a: &[f32;3], b: &[f32;3]) -> bool {
    pub_is_close(a[0], b[0]) && pub_is_close(a[1], b[1]) && pub_is_close(a[2], b[2])
}
fn pub_vec4_allclose(a: &[f32;4], b: &[f32;4]) -> bool {
    pub_is_close(a[0], b[0]) && pub_is_close(a[1], b[1]) && pub_is_close(a[2], b[2]) && pub_is_close(a[3], b[3])
}

#[test]
fn pub_test_vec2_mul_inner() {
    let mut v = [0.0; 2];
    pub_vec2_set(&mut v, 2.5);
    let inner = vec2_mul_inner(v, v);
    assert!(pub_is_close(inner, 2.0 * (2.5 * 2.5)));
}

#[test]
fn pub_test_vec3_mul_inner() {
    let v = [-3.0, 1.0, 2.0];
    let inner = vec3_mul_inner(v, v);
    assert!(pub_is_close(inner, 9.0 + 1.0 + 4.0));
}

#[test]
fn pub_test_vec4_mul_inner() {
    let v = [0.0, 0.5, -1.5, 3.5];
    let inner = vec4_mul_inner(v, v);
    assert!(pub_is_close(inner, 0.0*0.0 + 0.5*0.5 + 1.5*1.5 + 3.5*3.5));
}

#[test]
fn pub_test_vec2_len() {
    let v = [6.0, 8.0];
    let norm = vec2_len(v);
    assert!(pub_is_close(norm, 10.0));
}

#[test]
fn pub_test_vec3_len() {
    let v = [1.0, 2.0, 2.0];
    let norm = vec3_len(v);
    assert!(pub_is_close(norm, 3.0));
}

#[test]
fn pub_test_vec4_len() {
    let v = [1.0, 2.0, 2.0, 3.0];
    let norm = vec4_len(v);
    assert!(pub_is_close(norm, (1.0f32 + 4.0 + 4.0 + 9.0).sqrt()));
}

#[test]
fn pub_test_vec2_norm() {
    let v = [3.0, 4.0];
    let mut r = [0.0, 0.0];
    vec2_norm(&mut r, v);
    let norm = vec2_len(r);
    assert!(pub_is_close(norm, 1.0));
}

#[test]
fn pub_test_vec3_norm() {
    let v = [10.0, 0.0, 5.0];
    let mut r = [0.0, 0.0, 0.0];
    vec3_norm(&mut r, v);
    let norm = vec3_len(r);
    assert!(pub_is_close(norm, 1.0));
}

#[test]
fn pub_test_vec4_norm() {
    let v = [-2.0, 0.0, 0.0, 0.0];
    let mut r = [0.0; 4];
    vec4_norm(&mut r, v);
    let norm = vec4_len(r);
    assert!(pub_is_close(norm, 1.0));
}

#[test]
fn pub_test_vec3_mul_cross() {
    let a = [1.0, 0.0, 0.0];
    let b = [0.0, 0.0, 2.0];
    let mut r = [0.0; 3];
    vec3_mul_cross(&mut r, a, b);
    assert!(pub_is_close(r[0], 0.0));
    assert!(pub_is_close(r[1], -2.0));
    assert!(pub_is_close(r[2], 0.0));
}

#[test]
fn pub_test_vec3_reflect() {
    let v = [3.0, -2.0, 5.0];
    let n = [0.0, 1.0, 0.0];
    let mut r = [0.0; 3];
    vec3_reflect(&mut r, v, n);
    assert!(pub_is_close(r[0], 3.0));
    assert!(pub_is_close(r[1], 2.0));
    assert!(pub_is_close(r[2], 5.0));
}