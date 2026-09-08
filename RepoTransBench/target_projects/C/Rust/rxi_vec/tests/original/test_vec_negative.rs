// Translated from test/test_vec_negative.c: low-level/negative edge coverage
use rxi_vec::VecInt;

#[test]
fn test_vec_reserve_smaller_than_capacity() {
    let mut v = VecInt::with_capacity(4);
    for _ in 0..3 { v.push(0); }
    let old_cap = v.capacity();
    let r = v.reserve(2);
    assert_eq!(r, 0);
    assert_eq!(v.capacity(), old_cap);
}

#[test]
fn test_vec_reserve_realloc_fail_sim() {
    let mut v: VecInt = VecInt::new();
    // Impossible to OOM deterministically in Rust; check large reserve returns 0
    let r = v.reserve(0x7FFFFFFF);
    assert_eq!(r, 0);
}

#[test]
fn test_vec_reserve_po2_grow() {
    let mut v = VecInt::new();
    let r = v.reserve(5);
    assert_eq!(r, 0);
    assert!(v.capacity() >= 5);
}

#[test]
fn test_vec_compact_already_compact() {
    let mut v = VecInt::with_capacity(4);
    for _ in 0..4 { v.push(0); }
    let r = v.compact();
    assert_eq!(r, 0);
    assert_eq!(v.capacity(), v.len());
}

#[test]
fn test_vec_compact_shrink() {
    let mut v = VecInt::with_capacity(6);
    for &val in &[10, 20, 30, 40] { v.push(val); }
    // Shrink to fit after truncate
    v.truncate(4);
    let r = v.compact();
    assert_eq!(r, 0);
    assert_eq!(v.capacity(), v.len());
}

#[test]
fn test_vec_insert_middle() {
    let mut v = VecInt::with_capacity(8);
    for &i in &[1,2,3,4,5,6] { v.push(i); }
    v.insert(3, 0);
    assert_eq!(v.len(), 7);
    assert_eq!(v.data[3], 0);
}

#[test]
fn test_vec_insert_into_empty() {
    let mut v = VecInt::new();
    let r = v.insert(0, 123);
    assert_eq!(r, 0);
    assert_eq!(v.data[0], 123);
}

#[test]
fn test_vec_swap_valid() {
    let mut v = VecInt::new();
    v.push(1); v.push(2); v.push(3);
    v.swap(0, 2);
    assert_eq!(v.data[0], 3);
    assert_eq!(v.data[2], 1);
}

#[test]
fn test_vec_swap_oob_no_crash() {
    let mut v = VecInt::new();
    v.push(10); v.push(20);
    v.swap(usize::MAX, 2);
    // No panic, no effect
    assert_eq!(v.data[0], 10);
    assert_eq!(v.data[1], 20);
}

#[test]
fn test_vec_splice_full_delete() {
    let mut v = VecInt::new();
    v.push(7); v.push(8); v.push(9); v.push(10);
    v.splice(0, 4);
    assert_eq!(v.len(), 0);
}

#[test]
fn test_vec_splice_partial_delete() {
    let mut v = VecInt::new();
    v.push(1); v.push(2); v.push(3); v.push(4);
    v.splice(1, 2);
    assert_eq!(v.data[0], 1);
    assert_eq!(v.data[1], 4);
    assert_eq!(v.len(), 2);
}

#[test]
fn test_vec_swapsplice_middle() {
    let mut v = VecInt::new();
    v.push(5); v.push(6); v.push(7); v.push(8);
    v.swapsplice(1, 2);
    assert_eq!(v.len(), 2);
    assert_eq!(v.data[0], 5);
    assert_eq!(v.data[1], 8);
}

#[test]
fn test_vec_swapsplice_end_noop() {
    let mut v = VecInt::new();
    v.push(5); v.push(6); v.push(7);
    v.swapsplice(2, 10);
    assert_eq!(v.len(), 2);
    assert_eq!(v.data[0], 5);
    assert_eq!(v.data[1], 6);
}