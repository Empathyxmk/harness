//! Rust translation of source/Test/test_runner.c
//! Miscellaneous runner and edge case test.

#[test]
fn test_sum() {
    assert_eq!(1 + 1, 2);
}

#[test]
fn test_edge_case_zero() {
    let a = 0;
    assert_eq!(a, 0);
}