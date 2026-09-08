use lemire_fastrange::*;

#[test]
fn test_fastrange64_fallback_public() {
    // Testing fastrange64 with different 64-bit values
    let a = 998877665544332211u64;
    let b = 1234567890123456u64;
    assert!(fastrange64(a, 101) < 101);
    assert!(fastrange64(b, 7777) < 7777);
    assert!(fastrange64(9876543210123456789u64, 99999) < 99999);
    assert_eq!(fastrange64(0, 98765), 0);

    for i in (3..70).step_by(17) {
        let res = fastrange64(i*654321, i + 800);
        assert!(res < i + 800);
    }
}