use std::collections::HashMap;
use serde::{Serialize, Deserialize};
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
enum Color {
    RED,
    GREEN,
    BLUE,
}

#[test]
fn test_enum_serde_by_variant() {
    let color = Color::RED;
    let json = serde_json::to_string(&color).unwrap();
    let color2: Color = serde_json::from_str(&json).unwrap();
    assert_eq!(color, color2);
}

#[test]
fn test_basic_vec_and_map() {
    let v = vec!["foo".to_string(), "bar".to_string()];
    let json = serde_json::to_string(&v).unwrap();
    let v2: Vec<String> = serde_json::from_str(&json).unwrap();
    assert_eq!(v, v2);

    let mut m = HashMap::new();
    m.insert("foo".to_string(), "bar".to_string());
    let json = serde_json::to_string(&m).unwrap();
    let m2: HashMap<String, String> = serde_json::from_str(&json).unwrap();
    assert_eq!(m, m2);
}

// "Union"-like sum types, handled by enum in previous tests.