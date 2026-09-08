use jart_morton::{morton, unmorton};

#[test]
fn test_pattern_00ff00ff() {
    let xx = 0x00FF_00FF;
    let yy = 0xFF00_FF00;
    let z = morton(xx, yy);
    let m = unmorton(z);
    assert_eq!((m.lo, m.hi), (xx, yy));
}

#[test]
fn test_max_values() {
    let xx = 0xFFFFFFFEu32;
    let yy = 0x80000001u32;
    let z = morton(xx, yy);
    let m = unmorton(z);
    assert_eq!((m.lo, m.hi), (xx, yy));

    let z = morton(0x87654321u32, 0x12345678u32);
    let m = unmorton(z);
    assert_eq!((m.lo, m.hi), (0x87654321u32, 0x12345678u32));
}

#[test]
fn test_reverse() {
    let z = morton(0x0F0F0F0F, 0xF0F0F0F0);
    let m = unmorton(z);
    assert_eq!(m.lo, 0x0F0F0F0F);
    assert_eq!(m.hi, 0xF0F0F0F0);

    let z = morton(0x55555555, 0xAAAAAAAA);
    let m = unmorton(z);
    assert_eq!(m.lo, 0x55555555);
    assert_eq!(m.hi, 0xAAAAAAAA);
}

#[test]
fn test_single_bit_positions() {
    for k in 0..32 {
        let x = 1u32 << k;
        let y = 0u32;
        let z = morton(x, y);
        let m = unmorton(z);
        assert_eq!((m.lo, m.hi), (x, 0));

        let x = 0u32;
        let y = 1u32 << k;
        let z = morton(x, y);
        let m = unmorton(z);
        assert_eq!((m.lo, m.hi), (0, y));
    }
}

#[test]
fn test_unmorton_noncanonical() {
    let z = 0xDEADBEEF12345678u64;
    let m = unmorton(z);
    let z2 = morton(m.lo, m.hi);
    assert_eq!(m.lo, unmorton(z).lo);
    assert_eq!(m.hi, unmorton(z).hi);
}