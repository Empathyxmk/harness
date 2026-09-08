#[test]
fn test_public_main_true() {
    assert!(!vec![1].is_empty());
}

#[test]
fn test_public_main_value() {
    let s = String::from("hamms");
    assert!(s.is_ascii());
}