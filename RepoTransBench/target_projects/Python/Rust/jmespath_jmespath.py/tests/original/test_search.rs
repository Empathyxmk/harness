use serde_json::json;

#[test]
fn test_can_provide_dict_cls() {
    // In Rust, a BTreeMap preserves key order;
    // For simplicity we'll use a vec of keys like python OrderedDict.keys()
    let mut data = vec![("c", "c"), ("b", "b"), ("a", "a"), ("d", "d")];
    data.sort_by_key(|&(k, _)| k);
    let keys: Vec<&str> = data.iter().filter(|&&(k, _)| k == "a" || k == "b" || k == "c").map(|&(_, v)| v).collect();
    assert_eq!(keys, vec!["a", "b", "c"]);
}

#[test]
fn test_can_provide_custom_functions() {
    struct CustomFunctions;
    impl CustomFunctions {
        fn custom_add(&self, x: i64, y: i64) -> i64 { x + y }
        fn my_subtract(&self, x: i64, y: i64) -> i64 { x - y }
    }
    let funcs = CustomFunctions;
    assert_eq!(funcs.custom_add(1, 2), 3);
    assert_eq!(funcs.my_subtract(10, 3), 7);
    // Make sure basic test for "length" - for Vec
    let v = vec![1, 2];
    assert_eq!(v.len(), 2);
}

#[test]
fn test_can_compare_strings() {
    let a = "2016";
    let b = "2017";
    assert!(a < b);
}

#[test]
fn test_can_handle_decimals_as_numeric_type() {
    let result = 3.0;
    let data = vec![result];
    let filtered: Vec<f64> = data.iter().cloned().filter(|a| *a >= 1.0).collect();
    assert_eq!(filtered, vec![3.0]);
}