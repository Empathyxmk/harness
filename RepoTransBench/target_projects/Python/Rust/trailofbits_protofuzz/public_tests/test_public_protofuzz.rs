use crate::protofuzz;
use std::collections::HashMap;

#[test]
fn test_message_strategy_public() {
    // Use field "y" and value 42, check field is set
    let mut mapping: HashMap<&'static str, Box<dyn Fn(String, Option<String>) -> Box<dyn Iterator<Item = i32>>>> = HashMap::new();
    mapping.insert("y", Box::new(|_t, _f| Box::new(vec![42].into_iter())));
    let strat = protofuzz::message_strategy(protofuzz::SimpleNamespace::new_y, mapping);
    let mut g = strat();
    let msg = g.next().unwrap();
    assert!(matches!(msg.y, Some(42)));
}

#[test]
fn test_fuzz_public() {
    let strat = || Box::new(vec!["D".to_string(), "E".to_string(), "F".to_string()].into_iter());
    let mut results: Vec<String> = Vec::new();
    let collect = |msg: String| results.push(msg);
    protofuzz::fuzz(strat, collect, 3);
    assert_eq!(results, vec!["D", "E", "F"]);
}