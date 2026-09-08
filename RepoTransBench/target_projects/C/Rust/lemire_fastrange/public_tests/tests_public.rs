use lemire_fastrange::*;

#[test]
fn test_basic_public() {
    // Basic tests with different values
    assert_eq!(fastrange32(25, 3), 1);
    assert_eq!(fastrange32(50, 7), 8); // check for value within range
    assert!(fastrange32(u32::MAX-100, 12345) < 12345);
    assert_eq!(fastrange32(7, 5), 1);
    assert!(fastrange32(87654321, 54321) < 54321);

    // Edge and error cases with different data
    assert_eq!(fastrange32(2, 2), 1);
    assert!(fastrange32(u32::MAX-1, u32::MAX-1) < u32::MAX-1);
}