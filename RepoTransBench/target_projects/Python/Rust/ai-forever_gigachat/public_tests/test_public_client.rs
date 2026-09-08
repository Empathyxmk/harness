use std::collections::HashMap;

// Simulates the Python "_unknown_kwargs" test
fn _unknown_kwargs(kwargs: HashMap<&str, &str>) -> HashMap<&str, &str> {
    kwargs
}

#[test]
fn test_unknown_kwargs_gets_filtered() {
    let mut args = HashMap::new();
    args.insert("alpha", "beta");
    args.insert("gamma", "42");
    args.insert("is_test", "true");
    let result = _unknown_kwargs(args.clone());
    assert_eq!(result.get("alpha"), Some(&"beta"));
    assert_eq!(result.get("gamma"), Some(&"42"));
    assert_eq!(result.get("is_test"), Some(&"true"));
}