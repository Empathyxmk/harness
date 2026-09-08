use paulocode_picostation::utils::*;

#[test]
fn test_utils_public() {
    // Public Test: tobcd with different values
    assert_eq!(tobcd(1), 0x01);
    assert_eq!(tobcd(27), 0x27);
    assert_eq!(tobcd(53), 0x53);
    assert_eq!(tobcd(88), 0x88);

    // Public Test: reverseBits with different numbers
    assert_eq!(reverse_bits(0b01, 2), 0b10);
    assert_eq!(reverse_bits(0b110, 3), 0b011);
    assert_eq!(reverse_bits(0xAA, 8), 0x55);

    // Public Test: track_to_sector and sectors_per_track, different values
    assert_eq!(track_to_sector(15), 15);
    assert_eq!(sectors_per_track(7), 1);
}