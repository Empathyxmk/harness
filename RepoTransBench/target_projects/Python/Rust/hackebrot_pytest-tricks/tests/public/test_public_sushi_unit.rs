mod model_sushi;
use model_sushi::{Sushi, Restaurant};

#[test]
#[should_panic]
fn test_init_raises_value_error_if_ingredients_is_null() {
    Sushi::new("California Roll", vec![]).unwrap();
}

#[test]
#[should_panic]
fn test_init_raises_value_error_if_menu_is_null() {
    Restaurant::new("Sushiland", "Tokyo", None).unwrap();
}

#[test]
fn test_init_works_with_valid_data() {
    let r = Restaurant::new("Sushiland", "Osaka", Some(vec!["Kani Nigiri"])).unwrap();
    assert_eq!(r.menu, vec!["Kani Nigiri".to_string()]);
    let s = Sushi::new("Kani Nigiri", vec!["Crab", "Rice"]).unwrap();
    assert_eq!(s.name, "Kani Nigiri");
    assert!(s.contains("Crab"));
}

#[test]
fn test_contains_operator_false() {
    let sushi = Sushi::new("Avocado Roll", vec!["Avocado", "Rice", "Nori"]).unwrap();
    assert!(!sushi.contains("Cucumber"));
}

#[test]
fn test_contains_operator_true() {
    let sushi = Sushi::new("Avocado Roll", vec!["Avocado", "Rice", "Nori"]).unwrap();
    assert!(sushi.contains("Avocado"));
}

#[test]
fn test_is_vegetarian_property() {
    let cases = vec![
        (vec!["Avocado", "Rice", "Nori"], true),
        (vec!["Tuna", "Rice", "Nori"], false),
        (vec!["Egg", "Rice"], true),
        (vec!["Shrimp", "Rice"], false),
    ];
    for (ingredients, is_veg) in cases.iter() {
        let sushi = Sushi::new("Custom Roll", ingredients.clone()).unwrap();
        assert_eq!(sushi.is_vegetarian(), *is_veg);
    }
}