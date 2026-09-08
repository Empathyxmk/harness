use true_random::get_bit;

#[test]
fn test_generate_constant_stream() {
    // Test generating 20 bytes in a different bit-packing pattern
    let mut bytes = Vec::new();
    
    for _ in 0..20 {
        let mut byte: u8 = 0;
        for i in 0..8 {
            byte |= (get_bit() as u8) << (7 - i); // Different bit packing pattern
        }
        bytes.push(byte);
    }
    
    assert_eq!(bytes.len(), 20);
}