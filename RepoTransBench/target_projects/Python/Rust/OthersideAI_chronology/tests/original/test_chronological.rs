use chronology::dummy_add;

#[test]
fn test_dummy_add() {
    assert_eq!(dummy_add(2, 3), 5);
    assert_eq!(dummy_add(-1, 1), 0);
    assert_eq!(dummy_add(0, 0), 0);
}