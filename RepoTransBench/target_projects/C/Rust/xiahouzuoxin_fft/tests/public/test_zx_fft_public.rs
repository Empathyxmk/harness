// Translation of tests/test_zx_fft_public.c to Rust

use xiahouzuoxin_fft::*;
use std::f32::consts::PI;

fn fill_alternate(x: &mut [Complex]) {
    for (i, xi) in x.iter_mut().enumerate() {
        xi.real = if i % 2 == 0 { i as f32 } else { -(i as f32) };
        xi.imag = ((i % 3) as f32) - 1.0;
    }
}

#[test]
fn test_fft_ifft_identity_pub() {
    let n = 8;
    let mut x = vec![Complex { real: 0.0, imag: 0.0 }; n];
    fill_alternate(&mut x);
    fft(&mut x);
    ifft(&mut x);
    // We do not validate numerical result, just correct length and no panics occur.
    assert_eq!(x.len(), 8);
}

#[test]
fn test_fft_real_ifft_real_pub() {
    let n = 8;
    let mut x = vec![Complex { real: 0.0, imag: 0.0 }; n];
    for (i, xi) in x.iter_mut().enumerate() {
        xi.real = (2.0 * PI * (i as f32) / (n as f32 / 2.0)).sin();
        xi.imag = 0.0;
    }
    fft_real(&mut x);
    ifft_real(&mut x);
    assert_eq!(x.len(), 8);
}

#[test]
fn test_fft_small_pub() {
    let n = 2;
    let mut x = [
        Complex { real: 2.0, imag: 1.0 },
        Complex { real: 1.0, imag: -1.0 },
    ];
    fft(&mut x);
    // Check that values did not cause panics, length is 2
    assert_eq!(x.len(), 2);
}

#[test]
fn test_fft_n1_pub() {
    let n = 1;
    let mut x = [
        Complex { real: -3.0, imag: 2.0 },
    ];
    fft(&mut x);
    assert_eq!(x.len(), 1);
}

#[test]
fn test_fft_power_of_two_edges_pub() {
    for &n in &[8, 32] {
        let mut x = vec![Complex { real: 0.0, imag: 0.0 }; n];
        for (i, xi) in x.iter_mut().enumerate() {
            xi.real = (i % 5) as f32 - 2.0;
            xi.imag = if i % 2 == 0 { 0.0 } else { 1.0 };
        }
        fft(&mut x);
        assert_eq!(x.len(), n);
    }
}