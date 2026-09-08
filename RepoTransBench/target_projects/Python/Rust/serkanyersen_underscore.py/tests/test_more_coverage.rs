use serkanyersen_underscore::underscore::{is_empty, IsEmpty};

#[test]
fn test_is_empty() {
    let v: Vec<i32> = Vec::new();
    assert!(is_empty(&v));
    let v = vec![1];
    assert!(!is_empty(&v));
}