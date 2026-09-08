use std::collections::HashMap;
use wroberts_pytimeparse::pytimeparse::timeparse::{timeparse, _interpret_as_minutes};

#[test]
fn test_timeparse_hours_minutes_ambiguity() {
    let mut input_dict = HashMap::new();
    input_dict.insert("secs".to_string(), "24".to_string());
    input_dict.insert("mins".to_string(), "1".to_string());
    let out = _interpret_as_minutes("1:24", input_dict.clone());
    assert_eq!(out.get("hours").unwrap(), "1");
    assert_eq!(out.get("mins").unwrap(), "24");
    assert!(!out.contains_key("secs"));
}