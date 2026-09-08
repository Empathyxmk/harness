use chronology::dummy_positive;

#[test]
fn test_dummy_positive_public() {
    assert_eq!(dummy_positive(42), true);
    assert_eq!(dummy_positive(-17), false);
    assert_eq!(dummy_positive(0), false);
}