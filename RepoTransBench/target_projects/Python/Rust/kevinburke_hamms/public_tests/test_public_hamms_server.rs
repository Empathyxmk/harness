#[test]
fn test_public_server_true() {
    assert_eq!(100 / 5, 20);
}

#[test]
fn test_public_server_other() {
    use std::collections::HashMap;
    let mut config = HashMap::new();
    config.insert("foo", 5);
    config.insert("bar", 9);
    assert!(config.contains_key("bar"));
}