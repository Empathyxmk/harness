mod model_sushi;
use model_sushi::{Sushi, Restaurant};

#[test]
#[should_panic]
fn test_public_sushi_init_requires_ingredients() {
    Sushi::new("Rice Roll", vec![]).unwrap();
}

#[test]
#[should_panic]
fn test_public_restaurant_init_requires_menu() {
    Restaurant::new("Quick Sushi", "Naples", None).unwrap();
}