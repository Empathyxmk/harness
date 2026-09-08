use chronology::dummy_add;

#[test]
fn test_dummy_add_public() {
    assert_eq!(dummy_add(8, 4), 12);
    assert_eq!(dummy_add(-5, 10), 5);
    assert_eq!(dummy_add(7, -7), 0);
}