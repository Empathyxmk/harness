use jart_morton::{morton, unmorton};

#[test]
fn test_zero_one() {
    // All zeros
    assert_eq!(morton(0, 0), 0);
    let m0 = unmorton(0);
    assert_eq!((m0.lo, m0.hi), (0, 0));

    // All ones
    assert_eq!(morton(0xFFFFFFFF, 0xFFFFFFFF), 0xFFFFFFFFFFFFFFFFu64);
    let m1 = unmorton(0xFFFFFFFFFFFFFFFFu64);
    assert_eq!((m1.lo, m1.hi), (0xFFFFFFFF, 0xFFFFFFFF));
}

#[test]
fn test_low_edge() {
    assert_eq!(morton(0x1, 0x0), 0x2u64);
    let m = unmorton(0x2u64);
    assert_eq!((m.lo, m.hi), (0x1, 0x0));

    assert_eq!(morton(0x0, 0x1), 0x1u64);
    let m = unmorton(0x1u64);
    assert_eq!((m.lo, m.hi), (0x0, 0x1));
}

#[test]
fn test_high_edge() {
    assert_eq!(morton(0x80000000, 0), 0x8000_0000_0000_0000u64);
    assert_eq!(morton(0, 0x80000000), 0x4000_0000_0000_0000u64);
}

#[test]
fn test_bit_alternation() {
    let x = 0xAAAAAAAAu32;
    let y = 0x55555555u32;
    let z = morton(x, y);
    let m = unmorton(z);
    assert_eq!((m.lo, m.hi), (x, y));

    let x = 0x55555555u32;
    let y = 0xAAAAAAAAu32;
    let z = morton(x, y);
    let m = unmorton(z);
    assert_eq!((m.lo, m.hi), (x, y));
}

#[test]
fn test_known_cases() {
    assert_eq!(
        morton(0x12345678, 0xABCDEF01),
        morton(0x12345678, 0xABCDEF01)
    );
    let m = unmorton(morton(0xDEADBEEF, 0xBADF00D));
    assert_eq!((m.lo, m.hi), (0xDEADBEEF, 0xBADF00D));
}