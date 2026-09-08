use chronology::dummy_mul;

#[test]
fn test_dummy_mul_public() {
    assert_eq!(dummy_mul(4, 5), 20);
    assert_eq!(dummy_mul(-2, 6), -12);
    assert_eq!(dummy_mul(0, -3), 0);
}