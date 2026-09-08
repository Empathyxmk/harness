// Translation of tests/test_zx_math_public.c to Rust

use xiahouzuoxin_fft::*;

#[test]
fn test_dsp_max_min_val_pub() {
    let arr1 = [7.3, -4.8, 0.6, 2.2, 9.9];
    let (max1, min1) = dsp_max_min_val(&arr1);
    assert!((max1 - 9.9).abs() < 1e-5 && (min1 + 4.8).abs() < 1e-5);

    let arr2 = [42.42f32];
    let (max2, min2) = dsp_max_min_val(&arr2);
    assert!((max2 - 42.42).abs() < 1e-4 && (min2 - 42.42).abs() < 1e-4);

    let arr3 = [5.0, 5.0, 5.0];
    let (max3, min3) = dsp_max_min_val(&arr3);
    assert!((max3 - 5.0).abs() < 1e-4 && (min3 - 5.0).abs() < 1e-4);
}

#[test]
fn test_scale_pub() {
    let mut arr = [-1.0f32, 0.0, 1.0, 2.0];
    scale(&mut arr, 2.0, -1.0, 10.0, 20.0);
    let expected = [10.0, 13.333_333f32, 16.666_668f32, 20.0];
    for (a,b) in arr.iter().zip(expected.iter()) {
        assert!((a - b).abs() < 0.05);
    }

    let mut arr2 = [-3.14f32];
    scale(&mut arr2, -3.14, -3.14, -5.0, 5.0);
    assert!((arr2[0] + 5.0).abs() < 1e-3);

    let mut arr3 = [-100.0, 0.0, 100.0];
    scale(&mut arr3, 100.0, -100.0, 0.0, 10.0);
    let expected3 = [0.0, 5.0, 10.0];
    for (a,b) in arr3.iter().zip(expected3.iter()) {
        assert!((a - b).abs() < 0.05);
    }
}

#[test]
fn test_cabs_pub() {
    let mut x = Complex { real: 6.0, imag: 8.0 };
    let mag = zx_cabs(x);
    assert!((mag - 10.0).abs() < 1e-3);

    x = Complex{ real: 1.0, imag: 0.0};
    assert!((zx_cabs(x) - 1.0).abs() < 1e-8);

    x = Complex{ real: -9.0, imag: 12.0};
    assert!((zx_cabs(x) - 15.0).abs() < 1e-3);
}

#[test]
fn test_ones_32_pub() {
    assert_eq!(ones_32(0xAAAAAAAAu32), 16);
    assert_eq!(ones_32(0x0F0F0F0Fu32), 16);
    assert_eq!(ones_32(0x33333333u32), 16);
    assert_eq!(ones_32(2u32), 1);
    assert_eq!(ones_32(0x40000000u32), 1);
}

#[test]
fn test_floor_log2_32_pub() {
    assert_eq!(floor_log2_32(16u32), 4);
    assert_eq!(floor_log2_32(2u32), 1);
    assert_eq!(floor_log2_32(255u32), 7);
    assert_eq!(floor_log2_32(0x40000000u32), 30);
    assert_eq!(floor_log2_32(7u32), 2);
}