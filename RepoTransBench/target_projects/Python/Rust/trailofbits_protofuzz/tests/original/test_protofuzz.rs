use crate::protofuzz;
use std::collections::HashMap;

#[test]
fn test_message_strategy_smoke() {
    // Simulate equivalent of message_strategy with a struct yielding SimpleNamespace with x set.
    // Rust: Use our core lib's dummy logic
    let mut mapping: HashMap<&'static str, Box<dyn Fn(String, Option<String>) -> Box<dyn Iterator<Item = i32>>>> = HashMap::new();
    mapping.insert("x", Box::new(|_t, _f| Box::new(vec![1].into_iter())));
    let strat = protofuzz::message_strategy(protofuzz::SimpleNamespace::new_x, mapping);
    let mut g = strat();
    let msg = g.next().unwrap();
    assert!(matches!(msg.x, Some(1)));
}

#[test]
fn test_fuzz_smoke() {
    // Create dummy generator: yields "A", "B", "C"
    let strat = || Box::new(vec!["A".to_string(), "B".to_string(), "C".to_string()].into_iter());
    let mut results: Vec<String> = Vec::new();
    let collect = |msg: String| results.push(msg);
    protofuzz::fuzz(strat, collect, 3);
    assert_eq!(results, vec!["A", "B", "C"]);
}