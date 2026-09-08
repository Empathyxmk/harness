//! Rust translation of source/Test/test_runner_public.c
//! Miscellaneous public runner test with different logic.

#[test]
fn test_difference() {
    assert_eq!(3 - 1, 2);
}

#[test]
fn test_edge_case_negative() {
    let b = -1;
    assert_ne!(b, 0);
    assert_eq!(b, -1);
}