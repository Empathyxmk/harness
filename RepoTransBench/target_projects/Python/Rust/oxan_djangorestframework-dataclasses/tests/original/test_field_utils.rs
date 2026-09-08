use std::collections::HashMap;

#[test]
fn test_hashmap_lookup() {
    let mut mapping = HashMap::new();
    mapping.insert("k1", 1);
    mapping.insert("k2", 2);
    assert_eq!(mapping.get("k1"), Some(&1));
    assert_eq!(mapping.get("k2"), Some(&2));
    assert!(mapping.get("k3").is_none());
}