// Translated from C: tests/test_utils_public.c

use simdcomp::*;

#[test]
fn test_simdmin() {
    let arr1 = [100, 150, 20, 37];
    assert_eq!(simdmin(&arr1), 20);

    let arr2 = [300, 222, 444, 123];
    assert_eq!(simdmin(&arr2), 123);

    let arr3 = [1234, 5678, 9012, 3456];
    assert_eq!(simdmin(&arr3), 1234);

    let arr4 = [90, 80, 70, 60];
    assert_eq!(simdmin(&arr4), 60);
}

#[test]
fn test_simdmax() {
    let arr1 = [9, 99, 888, 7];
    assert_eq!(simdmax(&arr1), 888);

    let arr2 = [100, 84, 56, 120];
    assert_eq!(simdmax(&arr2), 120);

    let arr3 = [1111, 2222, 3333, 4444];
    assert_eq!(simdmax(&arr3), 4444);

    let arr4 = [17, 19, 11, 23];
    assert_eq!(simdmax(&arr4), 23);
}

#[test]
fn test_simdsum() {
    let arr1 = [1, 2, 3, 4];
    assert_eq!(simdsum(&arr1), 10);

    let arr2 = [5, 10, 15, 20];
    assert_eq!(simdsum(&arr2), 50);

    let arr3 = [0, 0, 0, 0];
    assert_eq!(simdsum(&arr3), 0);

    let arr4 = [1000, 2000, 3000, 4000];
    assert_eq!(simdsum(&arr4), 10000);
}

#[test]
fn test_simdbitcpy() {
    let src = [0xF0F0F0F0, 0x0F0F0F0F, 0xCCCCCCCC, 0x33333333];
    let mut dst = [0u32; 4];
    simdbitcpy(&mut dst, &src, 4);
    assert_eq!(dst, src);
}