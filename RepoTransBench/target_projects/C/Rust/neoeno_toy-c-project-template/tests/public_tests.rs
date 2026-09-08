use toy_project::add;

#[test]
fn test_add_basic_public() {
    assert_eq!(add(3, 5), 8);
    assert_eq!(add(-2, 2), 0);
    assert_eq!(add(10, -10), 0);
}

#[test]
fn test_add_edge_cases_public() {
    assert_eq!(add(123456, 654321), 777777);
    assert_eq!(add(-500, -500), -1000);
    assert_eq!(add(1073741823, 1073741824), 2147483647); // also INT_MAX for 32bit
}