use crate::ope::{OPE, ValueRange};

#[test]
fn test_order_guarantees() {
    let values = vec![0, 1, 2, 10, 28, 42, 1000, 1001, (1 << 15) - 1];
    let key = b"key";
    let cipher = OPE::new(key);
    let mut encrypted_values: Vec<i64> = values.iter().map(|&v| cipher.encrypt(v)).collect();
    let mut sorted = encrypted_values.clone();
    sorted.sort_unstable();
    sorted.dedup();
    assert_eq!(encrypted_values, sorted);
}

#[test]
fn test_ope_encrypt_decrypt() {
    let values = vec![-1000, -100, -20, -1, 0, 1, 10, 100, 314, 1337, 1338, 10000];
    let key = b"key";
    let in_range = ValueRange::new(-1000, 1 << 20);
    let out_range = ValueRange::new(-10000, 1 << 32);
    let cipher = OPE::with_ranges(key, in_range.clone(), out_range.clone());
    let encrypted_values: Vec<i64> = values.iter().map(|&v| cipher.encrypt(v)).collect();
    let cipher_dec = OPE::with_ranges(key, in_range.clone(), out_range.clone());
    for (value, encrypted) in values.iter().zip(encrypted_values.iter()) {
        let decrypted = cipher_dec.decrypt(*encrypted);
        assert_eq!(*value, decrypted);
    }
}

#[test]
fn test_ope_deterministic() {
    let values = vec![0, 314, 1337, 1338, 10000];
    let cipher = OPE::new(b"key-la-la");
    let encrypted_values_first: Vec<i64> = values.iter().map(|&v| cipher.encrypt(v)).collect();
    let encrypted_values_second: Vec<i64> = values.iter().map(|&v| cipher.encrypt(v)).collect();
    assert_eq!(encrypted_values_first, encrypted_values_second);
}

#[test]
fn test_dense_range() {
    let range_start = 0;
    let range_end = 1 << 15;
    let in_range = ValueRange::new(range_start, range_end);
    let out_range = in_range.copy();
    let key = b"123";
    let cipher = OPE::with_ranges(key, in_range.clone(), out_range.clone());
    let values = vec![0, 10, 20, 50, 100, 1000, 1 << 10, 1 << 15];
    for v in &values {
        assert_eq!(cipher.encrypt(*v), *v);
        assert_eq!(cipher.decrypt(*v), *v);
    }
    // Should panic (simulate by catching)
    let res = std::panic::catch_unwind(|| {
        OPE::with_ranges(key, ValueRange::new(0, 10), ValueRange::new(1, 2));
    });
    assert!(res.is_err());
}

#[test]
fn test_long_different_keys() {
    let key1 = b"\x12\x23\x34\x45\x56\x67\x78\x89\x90\x0A\xAB\xBC\xCD\xDE\xEF\xF0\x13\x14\x15\x16";
    let key2 = b"\x0A\xAB\xBC\xCD\xDE\xEF\xF0\x13\x14\x15\x16\x12\x23\x34\x45\x56\x67\x78\x89\x90\x12\x13";
    let ope1 = OPE::new(key1);
    let ope2 = OPE::new(key2);
    let values = vec![0, 1, 10, 100, 1000, 2000, 3000, 4000, 5000];
    for v in &values {
        assert_ne!(ope1.encrypt(*v), ope2.encrypt(*v));
    }
}

#[test]
fn test_encrypt_small_out_range_issue() {
    let cipher = OPE::with_ranges(
        b"fresh key",
        ValueRange::new(0, 2),
        ValueRange::new(2, 5),
    );
    assert!(cipher.encrypt(0) >= 2 && cipher.encrypt(0) <= 5);
    assert!(cipher.encrypt(1) >= 2 && cipher.encrypt(1) <= 5);
    assert!(cipher.encrypt(2) >= 2 && cipher.encrypt(2) <= 5);
}

#[test]
fn test_big_ranges() {
    let in_range = ValueRange::new(1 << 32, (1 << 33));
    let out_range = ValueRange::new(1 << 48, (1 << 49));
    let ope = OPE::with_ranges(b"test-big-ranges", in_range.clone(), out_range.clone());
    let mut plaintext = in_range.start;
    while plaintext <= in_range.end {
        let _ = ope.encrypt(plaintext);
        plaintext += 1 << 24;
    }
}

#[test]
fn test_huge_output_range() {
    let cipher = OPE::with_ranges(
        b"key11",
        ValueRange::new(0, 0),
        ValueRange::new(0, 1 << 65),
    );
    assert!(cipher.encrypt(0) >= 0);
}