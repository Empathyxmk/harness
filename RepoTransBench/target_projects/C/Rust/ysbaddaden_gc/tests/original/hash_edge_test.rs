#[test]
fn test_insert_and_delete_keys() {
    use std::collections::HashMap;
    let mut map = HashMap::new();
    map.insert("key1", "foo");
    map.insert("key2", "bar");
    assert_eq!(map.get("key1"), Some(&"foo"));
    assert_eq!(map.get("key2"), Some(&"bar"));
    map.insert("key2", "baz");
    assert_eq!(map.get("key2"), Some(&"baz"));
    map.remove("key2");
    assert_eq!(map.get("key2"), None);
    assert_eq!(map.get("key3"), None);
    map.insert("key2", "again");
    assert_eq!(map.get("key2"), Some(&"again"));
    map.remove("key1");
    map.remove("key2");
    assert!(map.is_empty());
}