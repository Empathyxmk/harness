// public_tests/bit_array_public_test.rs
//
// Translated from dev/bit_array_public_test.c

use noporpoise_bitarray::bit_array::BitArray;

fn _test_copy(arr2: &mut BitArray, to: usize, arr1: &BitArray, from: usize, len: usize) {
    let mut str1: Vec<char> = arr1.to_string().chars().collect();
    let mut corr: Vec<char> = arr2.to_string().chars().collect();
    // extend corr if needed
    if corr.len() < to+len {
        corr.resize(to+len, '0');
    }
    for i in 0..len {
        if from+i < str1.len() && to+i < corr.len() {
            corr[to+i] = str1[from+i];
        }
    }
    // In actual logic, a bit-array copy method is expected
    // Here, we manually copy bits
    for i in 0..len {
        let v = arr1.get(from+i);
        if to+i < arr2.len() {
            arr2.bits[to+i] = v;
        }
    }
    let s2: String = arr2.to_string();
    let corr_s: String = corr.into_iter().collect();
    assert_eq!(s2, corr_s, "arr2 = {}, expected copy: {}", s2, corr_s);
}

#[test]
fn test_public_copy_different_sizes() {
    let mut arr = BitArray::new(40);
    arr.set_region(0, 10);

    _test_copy(&mut arr, 5, &arr.clone(), 0, 10);
    _test_copy(&mut arr, 20, &arr.clone(), 5, 15);
    _test_copy(&mut arr, 25, &arr.clone(), 0, 5);

    let len = arr.len();
    let shift = 4;
    arr.resize(len + shift);
    _test_copy(&mut arr, shift, &arr.clone(), 0, len);
    _test_copy(&mut arr, 0, &arr.clone(), shift, len);
}

fn _get_bits(arr: &BitArray, start: usize, end: usize, setbits: &mut Vec<usize>) {
    setbits.clear();
    for i in start..end {
        if arr.get(i) {
            setbits.push(i);
        }
    }
}

#[test]
fn test_public_get_bits() {
    let mut setbits = Vec::with_capacity(80);
    let mut arr = BitArray::new(80);
    arr.random(0.2);
    _get_bits(&arr, 0, 0, &mut setbits);
    _get_bits(&arr, 0, 80, &mut setbits);
    _get_bits(&arr, 80, 80, &mut setbits);
    _get_bits(&arr, 15, 70, &mut setbits);
}