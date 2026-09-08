mod model_sushi;
use model_sushi::{Sushi, Restaurant};

#[test]
fn test_restaurant_init_valid() {
    let rest = Restaurant::new("Foo", "Bar", Some(vec!["Sushi1", "Sushi2"])).unwrap();
    assert_eq!(rest.name, "Foo");
    assert_eq!(rest.location, "Bar");
    assert_eq!(rest.menu, vec!["Sushi1".to_string(), "Sushi2".to_string()]);
}

#[test]
#[should_panic]
fn test_restaurant_init_no_menu_raises() {
    Restaurant::new("NoMenu", "Where", None).unwrap();
}

#[test]
fn test_sushi_init_valid() {
    let s = Sushi::new("Veggie", vec!["Cucumber", "Rice"]).unwrap();
    assert_eq!(s.name, "Veggie");
    assert_eq!(s.ingredients, vec!["Cucumber".to_string(), "Rice".to_string()]);
}

#[test]
#[should_panic]
fn test_sushi_init_no_ingredients_raises() {
    Sushi::new("Nothing", vec![]).unwrap();
}

#[test]
fn test_sushi_contains_true() {
    let s = Sushi::new("Veggie", vec!["Cucumber", "Rice"]).unwrap();
    assert!(s.contains("Cucumber"));
}

#[test]
fn test_sushi_contains_false() {
    let s = Sushi::new("Veggie", vec!["Cucumber", "Rice"]).unwrap();
    assert!(!s.contains("Avocado"));
}

#[test]
fn test_sushi_is_vegetarian_cases() {
    let cases = vec![
        (vec!["Rice", "Cucumber"], true),
        (vec!["Rice", "Crab"], false),
        (vec!["Salmon", "Rice"], false),
        (vec!["Shrimp", "Rice"], false),
        (vec!["Tuna", "Rice"], false),
        (vec!["Egg", "Nori"], true),
    ];
    for (ingredients, expected) in cases {
        let s = Sushi::new("Test", ingredients.clone()).unwrap();
        assert_eq!(s.is_vegetarian(), expected);
    }
}