#[test]
fn test_basic_math() {
    assert_eq!(1 + 1, 2);
    let v: Vec<i32> = vec![];
    assert!(v.is_empty() || v.len() == 0);
}