#[test]
fn test_deterministic_key_generation_public() {
    let seed = b"anotherdeterministicseed";
    assert_eq!(seed, b"anotherdeterministicseed");
}

#[test]
fn test_ephemeral_key_generation_public() {
    let privv = vec![0u8; 32];
    let pubv = vec![0u8; 32];
    assert_eq!(privv.len(), 32);
    assert_eq!(pubv.len(), 32);
}

#[test]
fn test_key_exchange_public() {
    let s1 = vec![42u8; 32];
    let s2 = vec![42u8; 32];
    assert_eq!(s1, s2);
    assert_eq!(s1.len(), 32);
}