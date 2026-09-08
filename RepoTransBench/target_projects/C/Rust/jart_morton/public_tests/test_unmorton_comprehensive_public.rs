use jart_morton::{morton, unmorton};

#[test]
fn test_pattern_public() {
    let xx = 0x0F0F0F0F;
    let yy = 0xF0F0F0F0;
    let z = morton(xx, yy);
    let m = unmorton(z);
    assert_eq!((m.lo, m.hi), (xx, yy));
}

#[test]
fn test_max_values_public() {
    let xx = 0x7FFFFFFFu32;
    let yy = 0x80000000u32;
    let z = morton(xx, yy);
    let m = unmorton(z);
    assert_eq!((m.lo, m.hi), (xx, yy));

    let z = morton(0x12345678, 0x87654321);
    let m = unmorton(z);
    assert_eq!((m.lo, m.hi), (0x12345678, 0x87654321));
}

#[test]
fn test_reverse_public() {
    let z = morton(0xAAAAAAAA, 0x55555555);
    let m = unmorton(z);
    assert_eq!(m.lo, 0xAAAAAAAA);
    assert_eq!(m.hi, 0x55555555);

    let z = morton(0x0F0F0F0F, 0x33333333);
    let m = unmorton(z);
    assert_eq!(m.lo, 0x0F0F0F0F);
    assert_eq!(m.hi, 0x33333333);
}

#[test]
fn test_single_bit_positions_public() {
    for k in 0..32 {
        let bitpos = ((31-k)&31) as u32;
        let x = 1u32 << bitpos;
        let y = 0u32;
        let z = morton(x, y);
        let m = unmorton(z);
        assert_eq!((m.lo, m.hi), (x, 0u32));

        let x = 0u32;
        let y = 1u32 << bitpos;
        let z = morton(x, y);
        let m = unmorton(z);
        assert_eq!((m.lo, m.hi), (0u32, y));
    }
}

#[test]
fn test_unmorton_noncanonical_public() {
    let z = 0xBAADF00DDEADBEEFu64;
    let m = unmorton(z);
    let _z2 = morton(m.lo, m.hi);
    assert_eq!(m.lo, unmorton(z).lo);
    assert_eq!(m.hi, unmorton(z).hi);
}