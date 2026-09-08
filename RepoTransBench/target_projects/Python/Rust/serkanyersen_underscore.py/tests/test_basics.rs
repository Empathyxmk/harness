use serkanyersen_underscore::underscore::identity;

#[test]
fn test_identity() {
    assert_eq!(identity(42), 42);
}