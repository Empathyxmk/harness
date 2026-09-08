mod model_sushi;
use model_sushi::{Restaurant, Sushi};

#[test]
#[should_panic]
fn test_restaurant_empty_menu_list_raises() {
    Restaurant::new("Foo", "Bar", Some(vec![])).unwrap();
}

#[test]
#[should_panic]
fn test_sushi_empty_ingredients_list_raises() {
    Sushi::new("Foo", vec![]).unwrap();
}