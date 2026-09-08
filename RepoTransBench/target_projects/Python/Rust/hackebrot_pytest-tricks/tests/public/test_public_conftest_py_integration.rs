mod model_sushi;
use model_sushi::Sushi;
use std::collections::HashMap;

fn recipes() -> HashMap<&'static str, Vec<&'static str>> {
    [
        ("spicytuna", vec!["tuna", "sriracha", "scallions"]),
        ("rainbow", vec!["tuna", "avocado", "shrimp", "salmon"]),
    ].into_iter().collect()
}

#[test]
fn test_conftest_py_recipe() {
    let recipes = recipes();
    let cases = [
        ("spicytuna", vec!["tuna", "sriracha", "scallions"]),
        ("rainbow", vec!["tuna", "avocado", "shrimp", "salmon"]),
    ];
    for (sushi, expect) in cases.iter() {
        let roll = Sushi::new(*sushi, expect.clone()).unwrap();
        assert_eq!(roll.ingredients, expect.iter().map(|s| s.to_string()).collect::<Vec<_>>());
    }
}