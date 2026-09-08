// Translation of tests/test_zx_math.c to Rust

use xiahouzuoxin_fft::*;

#[test]
fn test_dsp_max_min_val() {
    // Multiple test arrays
    let arr1 = [1.5, 2.5, -3.5, 8.2, 0.0];
    let (max1, min1) = dsp_max_min_val(&arr1);
    assert!((max1 - 8.2).abs() < 1e-5 && (min1 + 3.5).abs() < 1e-5);

    let arr2 = [0.0f32];
    let (max2, min2) = dsp_max_min_val(&arr2);
    assert!((max2 - 0.0).abs() < 1e-5 && (min2 - 0.0).abs() < 1e-5);

    let arr3 = [-2.0, -2.0, -2.0];
    let (max3, min3) = dsp_max_min_val(&arr3);
    assert!((max3 - (-2.0)).abs() < 1e-5 && (min3 - (-2.0)).abs() < 1e-5);
}

#[test]
fn test_scale() {
    // normal scaling
    let mut arr = [2.0, 4.0, 6.0, 8.0];
    scale(&mut arr, 8.0, 2.0, -1.0, 1.0);
    let expected = [-1.0, -0.333333343, 0.333333343, 1.0];
    for (a,b) in arr.iter().zip(expected.iter()) {
        assert!((a - b).abs() < 0.02);
    }

    // edge case: xmax == xmin
    let mut arr2 = [3.14f32];
    scale(&mut arr2, 3.14, 3.14, 0.0, 1.0);
    assert!((arr2[0] - 0.0).abs() < 1e-5);

    let mut arr3 = [0.0, 50.0, 100.0];
    scale(&mut arr3, 100.0, 0.0, -100.0, 100.0);
    let expected3 = [-100.0, 0.0, 100.0];
    for (a,b) in arr3.iter().zip(expected3.iter()) {
        assert!((a - b).abs() < 0.01);
    }
}

#[test]
fn test_cabs() {
    let mut x = Complex { real: 3.0, imag: 4.0 };
    let mag = zx_cabs(x);
    assert!((mag - 5.0).abs() < 1e-4);

    x = Complex{ real: 0.0, imag: 0.0};
    assert!((zx_cabs(x)).abs() < 1e-8);

    x = Complex{ real: -5.0, imag: 12.0};
    assert!((zx_cabs(x) - 13.0).abs() < 1e-3);
}

#[test]
fn test_ones_32() {
    assert_eq!(ones_32(0u32), 0);
    assert_eq!(ones_32(0xFFFFFFFFu32), 32);
    assert_eq!(ones_32(0xF0F0u32), 8);
    assert_eq!(ones_32(1u32), 1);
    assert_eq!(ones_32(0x80000000u32), 1);
}

#[test]
fn test_floor_log2_32() {
    assert_eq!(floor_log2_32(8u32), 3);
    assert_eq!(floor_log2_32(1u32), 0);
    assert_eq!(floor_log2_32(1023u32), 9);
    assert_eq!(floor_log2_32(0x80000000u32), 31);
    assert_eq!(floor_log2_32(3u32), 1);
}