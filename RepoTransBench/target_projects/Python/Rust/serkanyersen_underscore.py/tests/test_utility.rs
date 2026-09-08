use serkanyersen_underscore::underscore::random;

#[test]
fn test_random() {
    let num = random(1, 10);
    assert!(1 <= num && num <= 10);
}