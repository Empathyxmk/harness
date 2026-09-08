// Translated from C: tests/test_utils.c

use simdcomp::*;

#[test]
fn test_util_edge_cases() {
    // Edge: all zeros
    let zeros = [0u32; 128];
    assert_eq!(maxbits_length(&zeros, 128), 0);

    // Edge: all same value
    let mut vals = [0u32; 128];
    for v in vals.iter_mut() {
        *v = 77;
    }
    assert_eq!(maxbits_length(&vals, 128), 7); // 77 needs 7 bits

    // Edge: single value
    let oneval = [255u32; 1];
    assert_eq!(maxbits_length(&oneval, 1), 8);

    // simdmaxbitsd1, strictly increasing
    let mut a = [0u32; 128];
    a[0]=0; for i in 1..128 { a[i]=a[i-1]+1; }
    assert_eq!(simdmaxbitsd1(0, &a), 1);

    // simdmaxbitsd1 for large differences
    a[0] = 0; for i in 1..128 { a[i]=a[i-1]+10000; }
    let b = simdmaxbitsd1(0, &a);
    assert!(b > 0 && b <= 32);
}