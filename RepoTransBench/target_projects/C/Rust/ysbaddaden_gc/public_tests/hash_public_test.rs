#[test]
fn test_hash_insert_search_public() {
    use std::collections::HashMap;
    let mut h = HashMap::new();
    let key1 = 1001;
    let val1 = 5678;
    let key2 = 2002;
    let val2 = 1234;
    h.insert(key1, val1);
    h.insert(key2, val2);
    assert_eq!(h.get(&key1), Some(&val1));
    assert_eq!(h.get(&key2), Some(&val2));
    let key3 = 9999;
    assert_eq!(h.get(&key3), None);
}