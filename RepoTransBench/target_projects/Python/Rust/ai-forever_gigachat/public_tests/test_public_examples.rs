use ai_forever_gigachat::examples::{SimpleExample, SimpleFunctionExample};
use std::collections::HashMap;

#[test]
fn test_simple_example_repr_and_str() {
    let se = SimpleExample::new("Who created the Eiffel Tower?", "Gustave Eiffel built it in Paris.");
    assert!(se.q.starts_with("Who created"));
    assert!(se.a.ends_with("Paris."));
    let rep = format!("{:?}", se);
    assert!(rep.contains("Eiffel"));
}

#[test]
fn test_simple_function_example_repr_and_str() {
    let mut params = HashMap::new();
    params.insert("city".to_string(), "Tokyo".to_string());
    params.insert("year".to_string(), "2022".to_string());
    let sfe = SimpleFunctionExample::new("weather", params.clone(), "performed");
    assert_eq!(sfe.fn_name, "weather");
    assert_eq!(sfe.params["city"], "Tokyo");
    assert_eq!(sfe.out, "performed");
}