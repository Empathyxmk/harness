use lemire_fastrange::*;

#[test]
fn test_fastrange_extra() {
    // typical
    assert!(fastrange64(1234567890123u64, 1000) < 1000);
    assert_eq!(fastrange64(0, 42), 0);
    assert_eq!(fastrange64(1, 10), 0);
    // edge values
    assert!(fastrange64(u64::MAX, u32::MAX as u64) < u32::MAX as u64);
    assert!(fastrange64(u64::MAX, u64::MAX) <= u64::MAX);
    assert_eq!(fastrange64(0, u64::MAX), 0);
}