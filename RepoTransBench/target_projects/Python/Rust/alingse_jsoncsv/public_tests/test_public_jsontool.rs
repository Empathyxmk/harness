use serde_json::json;

#[test]
fn test_flatten_simple() {
    let input = json!({"a": {"b": 2}, "c": 3});
    let mut flat = std::collections::BTreeMap::new();
    flatten(&input, "", &mut flat);
    let mut expected = std::collections::BTreeMap::new();
    expected.insert("a.b".to_string(), json!(2));
    expected.insert("c".to_string(), json!(3));
    assert_eq!(flat, expected);
}

fn flatten(
    value: &serde_json::Value,
    prefix: &str,
    out: &mut std::collections::BTreeMap<String, serde_json::Value>,
) {
    match value {
        serde_json::Value::Object(map) => {
            for (k, v) in map.iter() {
                let new_prefix = if prefix.is_empty() { k.clone() } else { format!("{}.{}", prefix, k) };
                flatten(v, &new_prefix, out);
            }
        }
        _ => {
            out.insert(prefix.to_string(), value.clone());
        }
    }
}