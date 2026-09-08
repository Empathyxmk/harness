mod model_sushi;
use model_sushi::Sushi;
use std::collections::HashMap;

fn recipes() -> HashMap<&'static str, Vec<&'static str>> {
    [
        ("rainbow", vec!["tuna", "avocado", "shrimp", "salmon"]),
        ("spicytuna", vec!["tuna", "sriracha", "scallions"]),
    ].into_iter().collect()
}

#[test]
fn test_recipe_exists_for_roll() {
    let recipes = recipes();
    let rolls = ["rainbow", "spicytuna"];
    for roll in rolls.iter() {
        assert!(recipes.contains_key(roll));
        let s = Sushi::new(roll, recipes[roll].clone()).unwrap();
        assert_eq!(s.ingredients, recipes[roll].iter().map(|x| x.to_string()).collect::<Vec<_>>());
    }
}