use vijos_jd4::compare::{compare, strip_trailing_spaces_newlines};

#[test]
fn test_strip_trailing_spaces_newlines_public() {
    let s = "hello world    \n  \n\t";
    assert_eq!(strip_trailing_spaces_newlines(s), "hello world");
}

#[test]
fn test_compare_public_equal_norm() {
    let a = "foo bar   \n";
    let b = "foo bar";
    let eq = compare(a, b, true);
    assert!(eq);
}

#[test]
fn test_compare_public_not_equal() {
    let a = "value1";
    let b = "value2";
    let eq = compare(a, b, false);
    assert!(!eq);
}