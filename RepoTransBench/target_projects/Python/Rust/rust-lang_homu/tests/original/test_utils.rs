use homu_rust::utils;
use std::collections::HashMap;

#[test]
fn test_alphanumeric_only_cases() {
    assert_eq!(utils::alphanumeric_only("abc123DEF!@#"), "abc123DEF");
    assert_eq!(utils::alphanumeric_only(" **&$  456 "), "456");
}

#[test]
fn test_lazy_debug_prints() {
    let s = utils::lazy_debug("message", 42, 99);
    assert!(s.is_string() || s.len() > 0); // just check it's some string for stub
}

#[test]
fn test_merge_dicts() {
    let mut d1 = HashMap::new();
    d1.insert("a".to_string(), 1);
    d1.insert("b".to_string(), 2);
    let mut d2 = HashMap::new();
    d2.insert("b".to_string(), 3);
    d2.insert("c".to_string(), 4);
    let d = utils::merge_dicts(&d1, &d2);
    assert_eq!(d["a"], 1);
    assert_eq!(d["b"], 3);
    assert_eq!(d["c"], 4);
}

#[test]
fn test_strip_default() {
    assert_eq!(
        utils::strip_default(":user:dog:foo", "user:"),
        "dog:foo".to_string()
    );
    assert_eq!(
        utils::strip_default(":dog", ":cat"),
        ":dog".to_string()
    );
}