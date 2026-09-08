use toy_project::add;

#[test]
fn test_add_basic() {
    assert_eq!(add(1, 2), 3);
    assert_eq!(add(0, 0), 0);
    assert_eq!(add(-1, -1), -2);
}

#[test]
fn test_add_edge_cases() {
    assert_eq!(add(1000000, 1), 1000001);
    assert_eq!(add(-1000, 1000), 0);
    assert_eq!(add(2147483640, 7), 2147483647); // INT_MAX for 32bit
}