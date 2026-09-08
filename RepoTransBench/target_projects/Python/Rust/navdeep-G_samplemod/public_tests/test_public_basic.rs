use samplemod_rs::core::add;

#[test]
fn test_add_positive_numbers_public() {
    assert_eq!(add(10, 5), 15);
}

#[test]
fn test_add_negative_and_positive_public() {
    assert_eq!(add(-6, 4), -2);
}

#[test]
fn test_add_zero_public() {
    assert_eq!(add(0, 19), 19);
}