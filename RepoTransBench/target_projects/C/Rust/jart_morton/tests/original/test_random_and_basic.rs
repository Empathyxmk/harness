use jart_morton::{morton, unmorton};

fn rand32(seed: &mut u64) -> u32 {
    // Use Knuth's LCG, ported from the C source.
    *seed = seed.wrapping_mul(6364136223846793005u64);
    *seed = seed.wrapping_add(1442695040888963407u64);
    (*seed >> 32) as u32
}

#[test]
fn test_morton_basic() {
    assert_eq!(morton(0, 0), 0);
    assert_eq!(morton(0, 1), 1);
    assert_eq!(morton(1, 0), 2);
    assert_eq!(morton(1, 1), 3);
    assert_eq!(morton(0b0011, 0b0000), 0b1010);
    assert_eq!(morton(0b0000, 0b0011), 0b0101);
    assert_eq!(morton(0b1100, 0b0011), 0b1010_0101u64);

    assert_eq!(
        morton(0x347210d1u32, 0xc6843fadu32),
        0x5a346a180755e653u64
    );
}

#[test]
fn test_morton_random_roundtrip() {
    // Test many random combinations for roundtrip correctness
    let mut seed = 1u64;
    let n = 200;
    for _ in 0..n {
        let x = rand32(&mut seed);
        for _ in 0..n {
            let y = rand32(&mut seed);
            let z = morton(x, y);
            let m = unmorton(z);
            assert_eq!(m.lo, x);
            assert_eq!(m.hi, y);
        }
    }
}