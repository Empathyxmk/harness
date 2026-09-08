use serde_json::json;

struct CustomFunctions;

impl CustomFunctions {
    fn length0(&self, s: Option<&serde_json::Value>) -> usize {
        match s {
            Some(serde_json::Value::Null) | None => 0,
            Some(serde_json::Value::Array(ref arr)) => arr.len(),
            Some(serde_json::Value::Object(ref map)) => map.len(),
            Some(serde_json::Value::String(ref s)) => s.len(),
            _ => 0,
        }
    }
}

#[test]
fn test_null_to_nonetype() {
    let funcs = CustomFunctions;
    let data = json!({"a": {"b": [1, 2, 3]}});
    let a_b = data["a"]["b"].as_array();
    let a_c = data["a"].get("c");
    assert_eq!(funcs.length0(a_b.map(|_| &json!(vec![1, 2, 3]))), 3);
    assert_eq!(funcs.length0(a_c), 0);
}