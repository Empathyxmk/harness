use serde_json::json;

#[test]
fn test_compat_str_coercion() {
    let s = "public_example";
    assert_eq!(s, "public_example");
}

#[test]
fn test_compat_json_loads_dumps_branch() {
    let obj = json!({"a_pub": [5, 6], "b_pub": "YY"});
    let dumped = serde_json::to_string(&obj).unwrap();
    let loaded: serde_json::Value = serde_json::from_str(&dumped).unwrap();
    assert_eq!(obj, loaded);
}

#[test]
fn test_compat_map_and_zip_iterators() {
    let mut mapped: Vec<_> = [3, 4, 5].iter().map(|x| x - 1).collect();
    assert_eq!(mapped, [2, 3, 4]);
    let zipped: Vec<(_, _)> = [10, 20].iter().zip(["x", "y"].iter()).map(|(a, b)| (*a, *b)).collect();
    assert_eq!(zipped, [(10, "x"), (20, "y")]);
}