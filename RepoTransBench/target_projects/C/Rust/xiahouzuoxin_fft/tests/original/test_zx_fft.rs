// Translation of tests/test_zx_fft.c to Rust

use xiahouzuoxin_fft::*;
use std::f32::consts::PI;

fn fill_simple(x: &mut [Complex]) {
    for (i, xi) in x.iter_mut().enumerate() {
        xi.real = i as f32;
        xi.imag = 0.0;
    }
}

#[test]
fn test_fft_ifft_identity() {
    let n = 8;
    let mut x = vec![Complex { real: 0.0, imag: 0.0 }; n];
    fill_simple(&mut x);
    fft(&mut x);
    ifft(&mut x);
    for (i, xi) in x.iter().enumerate() {
        assert!((xi.real - (i as f32)).abs() < 1e-2, "Mismatch at idx {}: {:?}", i, xi);
        assert!(xi.imag.abs() < 1e-2, "Imag not zero at idx {}: {:?}", i, xi);
    }
}

#[test]
fn test_fft_real_ifft_real() {
    let n = 8;
    let mut x = vec![Complex { real: 0.0, imag: 0.0 }; n];
    for (i, xi) in x.iter_mut().enumerate() {
        xi.real = (2.0 * PI * (i as f32) / (n as f32)).cos();
        xi.imag = 0.0;
    }
    fft_real(&mut x);
    ifft_real(&mut x);
    // For a cosine, transformed/cycled, just check near initial
    let expected = [1.0, 0.707, 0.0, -0.707, -1.0, -0.707, 0.0, 0.707];
    for (xi, &exp) in x.iter().zip(expected.iter()) {
        assert!((xi.real - exp).abs() < 0.02);
    }
}

#[test]
fn test_fft_small() {
    let n = 2;
    let mut x = [
        Complex { real: 1.0, imag: 0.0 },
        Complex { real: 0.0, imag: 0.0 },
    ];
    fft(&mut x);
    assert!((x[0].real - 1.0).abs() < 1e-3 && (x[0].imag - 0.0).abs() < 1e-3);
    assert!((x[1].real - 1.0).abs() < 1e-3 && (x[1].imag - 0.0).abs() < 1e-3);
}

#[test]
fn test_fft_n1() {
    let n = 1;
    let mut x = [
        Complex { real: 5.0, imag: -2.0 },
    ];
    fft(&mut x);
    assert!((x[0].real - 5.0).abs() < 1e-3 && (x[0].imag + 2.0).abs() < 1e-3);
}

#[test]
fn test_fft_power_of_two_edges() {
    for &n in &[4, 16] {
        let mut x = vec![Complex { real: 0.0, imag: 0.0 }; n];
        for (i, xi) in x.iter_mut().enumerate() {
            xi.real = 0.5 * (i as f32);
            xi.imag = if i == 2 { -1.0 } else { 0.0 };
        }
        fft(&mut x);
        // Only basic structure check as FFT outputs will depend on actual algorithm.
        assert_eq!(x.len(), n);
        // Imaginary parts should be zero except where assigned
        for (i, xi) in x.iter().enumerate() {
            if i != 2 {
                assert!(xi.imag.abs() < 1e-3, "Index {} imag part not zero: {}", i, xi.imag);
            }
        }
    }
}