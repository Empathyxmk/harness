use chronology::dummy_positive;

#[test]
fn test_dummy_positive() {
    assert_eq!(dummy_positive(5), true);
    assert_eq!(dummy_positive(-3), false);
    assert_eq!(dummy_positive(0), false);
}