// This is a PUBLIC test file.
use serkanyersen_underscore::underscore::random;

#[test]
fn test_random_public() {
    let num = random(20, 25);
    assert!(20 <= num && num <= 25);
}