// This is a PUBLIC test file.
use std::collections::HashMap;
use serkanyersen_underscore::underscore::pairs;

#[test]
fn test_pairs_public() {
    let mut hm = HashMap::new();
    hm.insert("foo", 7);
    hm.insert("bar", 8);
    let mut result = pairs(&hm);
    result.sort_by(|a, b| a.0.cmp(&b.0));
    assert_eq!(result, vec![("bar", 8), ("foo", 7)]);
}