use crate::_version::{VERSION, VERSION_TUPLE};

#[test]
fn test_public_version_values() {
    assert_eq!(VERSION, VERSION);
    assert_eq!(VERSION_TUPLE, VERSION_TUPLE);
}

#[test]
fn test_public_version_struct() {
    assert!(VERSION.is_ascii());
    assert_eq!(VERSION, "9.9.9");
    assert_eq!(VERSION_TUPLE, (9,9,9));
}