#[test]
fn test_placeholder_middleware_core() {
    let mut map = std::collections::HashMap::new();
    map.insert("foo", 123);
    assert_eq!(map["foo"], 123);
}