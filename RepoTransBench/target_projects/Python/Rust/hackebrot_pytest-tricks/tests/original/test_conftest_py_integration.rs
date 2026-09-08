mod model_sushi;
use model_sushi::{Restaurant, Sushi};
use std::collections::HashMap;

fn fooshi_bar() -> Restaurant {
    Restaurant::new(
        "Fooshi Bar",
        "Buenos Aires",
        Some(vec![
            "Ebi Nigiri", "Edamame", "Inarizushi", "Kappa Maki",
            "Miso Soup", "Sake Nigiri", "Tamagoyaki"
        ])
    ).unwrap()
}

fn recipes_map() -> HashMap<&'static str, Vec<&'static str>> {
    [
        ("California Roll", vec!["Rice", "Cucumber", "Avocado", "Crab"]),
        ("Ebi Nigiri", vec!["Shrimp", "Rice"]),
        ("Inarizushi", vec!["Fried tofu", "Rice"]),
        ("Kappa Maki", vec!["Cucumber", "Rice", "Nori"]),
        ("Maguro Nigiri", vec!["Tuna", "Rice", "Nori"]),
        ("Sake Nigiri", vec!["Salmon", "Rice", "Nori"]),
        ("Tamagoyaki", vec!["Fried egg", "Rice", "Nori"]),
        ("Tsunamayo Maki", vec!["Tuna", "Mayonnaise"])
    ].into_iter().collect()
}

#[test]
fn test_fooshi_bar_fixture() {
    let f = fooshi_bar();
    assert_eq!(f.name, "Fooshi Bar");
    assert!(f.menu.contains(&"Ebi Nigiri".to_string()));
    assert_eq!(f.location, "Buenos Aires");
    assert!(f.menu.contains(&"Tamagoyaki".to_string()));
}

#[test]
fn test_recipes_fixture() {
    let recipes = recipes_map();
    assert!(recipes.contains_key("Ebi Nigiri"));
    let cal = recipes.get("California Roll").unwrap();
    assert_eq!(cal, &vec!["Rice", "Cucumber", "Avocado", "Crab"]);
}

fn sushi_fixture_param(sushi_name: &str) -> Sushi {
    let recipes = recipes_map();
    Sushi::new(sushi_name, recipes[sushi_name].clone()).unwrap()
}

#[test]
fn test_sushi_fixture_param() {
    let names = ["California Roll", "Ebi Nigiri", "Tamagoyaki"];
    for n in names.iter() {
        let sushi = sushi_fixture_param(n);
        assert!(["California Roll", "Ebi Nigiri", "Tamagoyaki"].contains(&sushi.name.as_str()));
        assert!(!sushi.ingredients.is_empty());
    }
}