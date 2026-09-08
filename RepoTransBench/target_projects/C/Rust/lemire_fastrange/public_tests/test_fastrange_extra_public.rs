use lemire_fastrange::*;

#[test]
fn test_fastrange_extra_public() {
    // Different values to test different random and edge cases
    assert_eq!(fastrange32(555, 99), (((555u64 * 99u64) >> 32) as u32));
    assert!(fastrange32(123456, 77) < 77);
    assert!(fastrange32(0xDEADBEEF, 10000) < 10000);
    assert!(fastrange32(0x7FFFFFFF, 10) < 10);

    for i in (1..51).step_by(11) {
        let res = fastrange32(i*12345, i + 352);
        assert!(res < i + 352);
    }
}