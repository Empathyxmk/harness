use true_random::{get_bit, get_byte};

#[test]
fn test_get_bit() {
    // Run get_bit 16 times, check return is 0 or 1
    for _ in 0..16 {
        let bit = get_bit();
        assert!(bit == 0 || bit == 1);
        // Optional debug output
        // println!("get_bit() = {}", bit);
    }
}

#[test]
fn test_get_byte() {
    // Run get_byte 4 times, just check function does not crash
    for _ in 0..4 {
        let b = get_byte();
        // println!("get_byte() = 0x{:02x}", b);
        let _ = b; // Use the variable to avoid compiler warnings
    }
}