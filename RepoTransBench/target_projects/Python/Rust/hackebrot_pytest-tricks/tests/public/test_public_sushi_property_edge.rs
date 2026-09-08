mod model_sushi;
use model_sushi::Sushi;

#[test]
fn test_public_is_vegetarian_edge_cases() {
    let cases = [
        (vec!["Carrot", "Rice", "Nori"], true),
        (vec!["Ham", "Rice"], true),
        (vec!["Tuna", "Rice"], false),
        (vec!["Salmon", "Nori", "Rice"], false),
    ];
    for (ingredients, expected) in cases.iter() {
        let sushi = Sushi::new("Edge Roll", ingredients.clone()).unwrap();
        assert_eq!(sushi.is_vegetarian(), *expected);
    }
}