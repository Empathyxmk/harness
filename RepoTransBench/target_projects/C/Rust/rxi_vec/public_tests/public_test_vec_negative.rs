// Translated from test/public_test_vec_negative.c (public negative tests)
use rxi_vec::VecInt;

macro_rules! my_assert {
    ($cond:expr) => {
        if !$cond {
            panic!("[FAIL] {}:{}: {}", file!(), line!(), stringify!($cond));
        }
    };
}

#[test]
fn test_vec_pop_empty_public() {
    let mut v = VecInt::new();
    let _ret = v.pop(); // value undefined, should not panic
    my_assert!(v.len() == 0);
}

#[test]
fn test_vec_remove_out_of_bounds_public() {
    let mut v = VecInt::new();
    for i in 0..7 { v.push(i + 100); }
    let before = v.len();
    // remove an invalid index (no-op; our remove by value, so removing value not present)
    v.remove(9999);
    my_assert!(v.len() == before);
}

#[test]
fn test_vec_insert_negative_public() {
    let mut v = VecInt::new();
    // In C, (size_t)-1 is a huge number == usize::MAX here. Should insert at end.
    v.insert(usize::MAX, 444);
    my_assert!(v.len() == 1);
    my_assert!(v.data[0] == 444);
}

#[test]
fn test_vec_truncate_large_public() {
    let mut v = VecInt::new();
    for i in 0..4 { v.push(i); }
    v.truncate(99); // Should not grow, should do nothing
    my_assert!(v.len() == 4);
}