use crate::jsons;

#[test]
fn test_tuple_dump_public() {
    let t = (11, "world", 3.5f64);
    let dumped = jsons::dump(&t);
    assert_eq!(dumped, serde_json::json!([11, "world", 3.5]));
}

#[test]
fn test_tuple_load_public() {
    let data = serde_json::json!([42, "foo", 1.25]);
    let loaded: (i32, String, f64) = jsons::load(data);
    assert_eq!(loaded, (42, "foo".to_string(), 1.25));
}