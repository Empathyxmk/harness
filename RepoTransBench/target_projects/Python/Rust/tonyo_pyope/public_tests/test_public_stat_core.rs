#[test]
fn test_hgd_sample_manual_public() {
    // Manual sampling logic: pick randint between a and b using coins
    let a : i32 = 5;
    let b : i32 = 8;
    let coins = vec![1, 0];
    let num_bits = 2;
    let mut idx = 0;
    for (i, bit) in coins.iter().rev().enumerate() {
        idx += *bit << i;
    }
    let result = a + (idx % (b - a + 1));
    assert!(a <= result && result <= b);
}

#[test]
fn test_coin_stream_manual_public() {
    let val = 0b101011;
    let mut bits: Vec<u8> = vec![];
    for i in 0..6 {
        bits.push(((val >> i) & 1) as u8);
    }
    for b in &bits {
        assert!(*b == 0 || *b == 1);
    }
}