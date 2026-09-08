use dfu_programmer::libdfu::libdfu_dummy;

#[test]
fn test_dummy_success_path() {
    assert_eq!(libdfu_dummy(200), 201); // If dummy adds 1 to input
    assert_eq!(libdfu_dummy(-10), -9);  // Negative input
}

#[test]
fn test_dummy_edge_cases() {
    assert_eq!(libdfu_dummy(0), 1);
    assert_eq!(libdfu_dummy(999), 1000); // Large positive value
}