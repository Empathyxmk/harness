mod model_sushi;
use model_sushi::Sushi;

#[test]
fn test_is_vegetarian_with_all_nonveg() {
    let s = Sushi::new("Mix",
         vec!["Crab", "Salmon", "Shrimp", "Tuna", "Rice"]).unwrap();
    assert!(!s.is_vegetarian());
}

#[test]
fn test_is_vegetarian_with_mixed_case() {
    let s = Sushi::new("Strange",
        vec!["crab", "salmon", "shrimp", "tuna"]).unwrap();
    // Case-sensitive: None matches "Crab" etc., so vegetarian
    assert!(s.is_vegetarian());
}