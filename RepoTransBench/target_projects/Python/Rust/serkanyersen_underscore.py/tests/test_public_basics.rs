// This is a PUBLIC test file.
use serkanyersen_underscore::underscore::identity;

#[test]
fn test_identity_public() {
    assert_eq!(identity("underscore".to_string()), "underscore".to_string());
}