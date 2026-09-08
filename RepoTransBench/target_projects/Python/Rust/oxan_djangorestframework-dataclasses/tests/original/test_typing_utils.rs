#[test]
fn test_vec_iterable_roundtrip() {
    let v = vec![1, 2, 3];
    let json = serde_json::to_string(&v).unwrap();
    let v2: Vec<i32> = serde_json::from_str(&json).unwrap();
    assert_eq!(v, v2);
}

#[test]
fn test_option_is_some_roundtrip() {
    let o = Some(3);
    let json = serde_json::to_string(&o).unwrap();
    let o2: Option<i32> = serde_json::from_str(&json).unwrap();
    assert_eq!(o, o2);
}