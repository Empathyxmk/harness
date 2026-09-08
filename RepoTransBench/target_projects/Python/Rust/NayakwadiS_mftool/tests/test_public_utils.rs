#[test]
fn test_basic_math_public() {
    assert_eq!(2 * 3, 6);
    use std::collections::HashMap;
    let m: HashMap<String, String> = HashMap::new();
    assert!(m.is_empty());
}