use lemire_fastrange::*;

#[test]
fn test_basic() {
    // Basic tests
    assert_eq!(fastrange32(10, 1), 0);
    assert_eq!(fastrange32(0, 100), 0);
    assert!(fastrange32(u32::MAX, 100) < 100);
    assert_eq!(fastrange32(0, 1), 0);
    assert!(fastrange32(12345678, 100000) < 100000);

    // Edge and error cases
    assert_eq!(fastrange32(1, 1), 0);
    assert!(fastrange32(u32::MAX, u32::MAX) <= u32::MAX);
}