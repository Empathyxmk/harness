use std::collections::HashMap;
use serkanyersen_underscore::underscore::keys;

#[test]
fn test_keys() {
    let mut hm = HashMap::new();
    hm.insert("a", 1);
    hm.insert("b", 2);
    let result = keys(&hm);
    assert!(result.contains("a"));
    assert!(result.contains("b"));
    assert_eq!(result.len(), 2);
}