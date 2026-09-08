use lemire_fastrange::*;

#[test]
fn test_fastrange_sizeint_public() {
    // Test with new SIZE_MAX-suitable range and different word, p
    let mut p = 10;
    while p <= 100 {
        let val = fastrangesize(p*999, p);
        assert!(val < p);
        p *= 2;
    }
    
    assert!(fastrangesize(17, 8) < 8);
    assert!(fastrangesize(usize::MAX-10, 21) < 21);
    assert_eq!(fastrangesize(77, 77), 0);
}