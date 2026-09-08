use std::collections::HashMap;
use serkanyersen_underscore::underscore::pairs;

#[test]
fn test_pairs() {
    let mut hm = HashMap::new();
    hm.insert("a", 1);
    hm.insert("b", 2);
    let mut result = pairs(&hm);
    result.sort_by(|a, b| a.0.cmp(&b.0));
    assert_eq!(result, vec![("a", 1), ("b", 2)]);
}