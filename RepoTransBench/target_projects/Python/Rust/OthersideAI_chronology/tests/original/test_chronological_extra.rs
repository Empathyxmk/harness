use chronology::dummy_mul;

#[test]
fn test_dummy_mul() {
    assert_eq!(dummy_mul(2, 3), 6);
    assert_eq!(dummy_mul(-1, 1), -1);
    assert_eq!(dummy_mul(0, 5), 0);
}