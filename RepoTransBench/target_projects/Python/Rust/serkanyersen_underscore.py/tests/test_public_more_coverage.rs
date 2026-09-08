// This is a PUBLIC test file.
use std::collections::HashMap;
use serkanyersen_underscore::underscore::{is_empty, IsEmpty};

#[test]
fn test_is_empty_public() {
    let map: HashMap<String, String> = HashMap::new();
    assert!(is_empty(&map));
    let mut nonempty = HashMap::new();
    nonempty.insert("a".to_string(), "z".to_string());
    assert!(!is_empty(&nonempty));
}