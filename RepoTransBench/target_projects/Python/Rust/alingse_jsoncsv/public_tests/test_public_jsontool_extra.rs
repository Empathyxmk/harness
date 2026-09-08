use serde_json::json;

#[test]
fn test_json_unflatten() {
    let mut flat = std::collections::BTreeMap::new();
    flat.insert("foo.bar".to_string(), json!(123));
    flat.insert("x".to_string(), json!(9));

    let result = unflatten(flat);

    let expected = json!({"foo": {"bar": 123}, "x": 9});
    assert_eq!(result, expected);
}

fn unflatten(mut map: std::collections::BTreeMap<String, serde_json::Value>) -> serde_json::Value {
    let mut root = serde_json::Map::new();
    for (k, v) in map.drain() {
        let mut keys: Vec<&str> = k.split('.').collect();
        let last = keys.pop().unwrap();
        let mut cursor = &mut root;
        for part in keys {
            cursor = cursor.entry(part).or_insert_with(|| serde_json::Value::Object(Default::default()))
                .as_object_mut().unwrap();
        }
        cursor.insert(last.to_owned(), v);
    }
    serde_json::Value::Object(root)
}