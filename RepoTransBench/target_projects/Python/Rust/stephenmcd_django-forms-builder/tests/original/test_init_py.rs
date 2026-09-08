use crate::forms_builder::__VERSION__;

#[test]
fn test_version_string() {
    let v = __VERSION__;
    assert!(v.chars().all(|c| c.is_ascii() && (c.is_digit(10) || c == '.')));
    assert_eq!(v.chars().filter(|&c| c == '.').count(), 2);
}