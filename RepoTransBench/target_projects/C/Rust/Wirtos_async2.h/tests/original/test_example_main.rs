use async2::example_entry;

#[test]
fn test_example() {
    // Basic entry, testing at least one path
    let ret = example_entry();
    assert!(ret == 42);
}