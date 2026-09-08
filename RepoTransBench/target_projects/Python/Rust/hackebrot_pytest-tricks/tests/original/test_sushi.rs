mod model_sushi;
use model_sushi::Sushi;

fn fooshi_bar_menu() -> Vec<&'static str> {
    vec![
        "Ebi Nigiri",
        "Edamame",
        "Inarizushi",
        "Kappa Maki",
        "Miso Soup",
        "Sake Nigiri",
        "Tamagoyaki"
    ]
}

fn sushi_from_name(name: &str) -> Sushi {
    let recipes = [
        ("Kappa Maki", vec!["Cucumber", "Rice", "Nori"]),
        ("Tamagoyaki", vec!["Fried egg", "Rice", "Nori"]),
        ("Inarizushi", vec!["Fried tofu", "Rice"]),
    ];
    let ingredients = recipes.iter()
        .find(|(n, _)| n == &name)
        .unwrap()
        .1
        .clone();
    Sushi::new(name, ingredients).unwrap()
}

#[test]
fn test_fooshi_serves_vegetarian_sushi() {
    let menu = fooshi_bar_menu();
    let sushi_names = ["Kappa Maki", "Tamagoyaki", "Inarizushi"];
    let side_dishes = ["Edamame", "Miso Soup"];
    for s in sushi_names.iter() {
        let sushi = sushi_from_name(s);
        assert!(sushi.is_vegetarian());
        assert!(menu.contains(&sushi.name.as_str()));
        for side in side_dishes.iter() {
            assert!(menu.contains(side));
        }
    }
}

#[test]
fn test_sushi_fields() {
    let s = sushi_from_name("Kappa Maki");
    assert!(!s.name.is_empty());
    assert!(!s.ingredients.is_empty());
}