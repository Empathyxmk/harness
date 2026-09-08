use paulocode_picostation::utils::*;

#[test]
fn test_utils_full() {
    // Test tobcd
    assert_eq!(tobcd(0), 0x00);
    assert_eq!(tobcd(15), 0x15);
    assert_eq!(tobcd(45), 0x45);
    assert_eq!(tobcd(99), 0x99);

    // Test reverseBits
    assert_eq!(reverse_bits(0b10, 2), 0b01);
    assert_eq!(reverse_bits(0b101, 3), 0b101);
    assert_eq!(reverse_bits(0xF0, 8), 0x0F);

    // track_to_sector and sectors_per_track
    assert_eq!(track_to_sector(8),8);
    assert_eq!(sectors_per_track(5),1);
}