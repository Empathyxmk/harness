// This is a PUBLIC test file.
use std::collections::HashMap;
use serkanyersen_underscore::underscore::keys;

#[test]
fn test_keys_public() {
    let mut hm = HashMap::new();
    hm.insert("x", 42);
    hm.insert("y", 100);
    let result = keys(&hm);
    assert_eq!(result.len(), 2);
    assert!(result.contains("x"));
    assert!(result.contains("y"));
}