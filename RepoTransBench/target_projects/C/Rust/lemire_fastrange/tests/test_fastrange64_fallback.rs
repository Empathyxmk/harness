use lemire_fastrange::*;

#[test]
fn test_fastrange64_fallback() {
    // These calls may trigger fallback code if present in fastrange.h
    let max = u64::MAX;
    let m = 12345u64;
    assert!(fastrange64(max, m) < m);
    assert_eq!(fastrange64(0, m), 0);

    if m > 1 {
        assert!(fastrange64(max, m - 1) < (m - 1));
    }
}