use jart_morton::{morton, unmorton};

#[test]
fn test_zero_one_public() {
    // All zeros
    assert_eq!(morton(0, 0), 0);
    let m0 = unmorton(0);
    assert_eq!((m0.lo, m0.hi), (0, 0));

    // All half-ones
    assert_eq!(
        morton(0xAAAAAAAA, 0x55555555),
        0xFFFFFFFFFFFFFFFFu64 / 3
    );
    let m1 = unmorton(0xFFFFFFFFFFFFFFFFu64 / 3);
    assert_eq!((m1.lo, m1.hi), (0xAAAAAAAA, 0x55555555));
}

#[test]
fn test_low_edge_public() {
    assert_eq!(morton(0x2, 0x1), 0x6u64);
    let m = unmorton(0x6u64);
    assert_eq!((m.lo, m.hi), (0x2, 0x1));

    assert_eq!(morton(0x3, 0x4), 0x1B);
    let m = unmorton(0x1B);
    assert_eq!((m.lo, m.hi), (0x3, 0x4));
}

#[test]
fn test_high_edge_public() {
    assert_eq!(morton(0x40000000, 0), 0x2000000000000000u64);
    assert_eq!(morton(0, 0x40000000), 0x1000000000000000u64);
}

#[test]
fn test_bit_alternation_public() {
    let mut x = 0x33333333u32;
    let mut y = 0xCCCCCCCCu32;
    let mut z = morton(x, y);
    let mut m = unmorton(z);
    assert_eq!((m.lo, m.hi), (x, y));

    x = 0x0F0F0F0Fu32;
    y = 0xF0F0F0F0u32;
    z = morton(x, y);
    m = unmorton(z);
    assert_eq!((m.lo, m.hi), (x, y));
}

#[test]
fn test_known_cases_public() {
    assert_eq!(
        morton(0x1A2B3C4D, 0x5E6F7081),
        morton(0x1A2B3C4D, 0x5E6F7081)
    );
    let m = unmorton(morton(0xCAFEBABE, 0xDEADC0DE));
    assert_eq!((m.lo, m.hi), (0xCAFEBABE, 0xDEADC0DE));
}