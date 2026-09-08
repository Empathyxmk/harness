use crate::version::VERSION;

#[test]
fn test_public_importable() {
    assert!(!VERSION.is_empty());
}