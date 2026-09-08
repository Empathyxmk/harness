use lemire_fastrange::*;

#[test]
fn test_fastrange_size_t() {
    // 32-bit or 64-bit size_t
    assert!(fastrangesize(25, 7) < 7);
    // Edge cases
    assert_eq!(fastrangesize(0, 5), 0);
    assert_eq!(fastrangesize(1, 1), 0);
    assert!(fastrangesize(usize::MAX, 100) < 100);
    assert!(fastrangesize(usize::MAX, usize::MAX) <= usize::MAX);
}