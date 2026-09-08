use crate::ope::{OPE, ValueRange};

#[test]
fn test_order_guarantees_public() {
    let in_range = ValueRange::new(10, 100);
    let out_range = ValueRange::new(200, 400);
    let key = b"pubkeytest";
    let cipher = OPE::with_ranges(key, in_range.clone(), out_range.clone());
    let values = vec![10, 20, 35, 49, 58, 60, 75, 80, 90, 100];
    let encrypted_values: Vec<i64> = values.iter().map(|&v| cipher.encrypt(v)).collect();
    for (&a, &b) in encrypted_values.iter().zip(encrypted_values[1..].iter()) {
        assert!(a < b);
    }
}

#[test]
fn test_invertibility_public() {
    let key = b"pubkeytest";
    let in_range = ValueRange::new(10, 25);
    let out_range = ValueRange::new(100, 1000);
    let cipher = OPE::with_ranges(key, in_range.clone(), out_range.clone());
    let values = vec![12, 13, 18, 20, 25];
    for v in values {
        let encrypted = cipher.encrypt(v);
        let decrypted = cipher.decrypt(encrypted);
        assert_eq!(decrypted, v);
    }
}

#[test]
fn test_edge_values_public() {
    let key = b"pubkeytest2";
    let in_range = ValueRange::new(0, 50);
    let out_range = ValueRange::new(500, 2000);
    let cipher = OPE::with_ranges(key, in_range.clone(), out_range.clone());
    for v in vec![0, 25, 50] {
        let encrypted = cipher.encrypt(v);
        let decrypted = cipher.decrypt(encrypted);
        assert_eq!(decrypted, v);
    }
}

#[test]
fn test_random_key_public() {
    let value = 30;
    let in_range = ValueRange::new(10, 40);
    let out_range = ValueRange::new(100, 900);
    let key1 = b"k1_random_diff";
    let key2 = b"k2_pub_diff";
    let cipher1 = OPE::with_ranges(key1, in_range.clone(), out_range.clone());
    let cipher2 = OPE::with_ranges(key2, in_range, out_range);
    let enc1 = cipher1.encrypt(value);
    let enc2 = cipher2.encrypt(value);
    assert_ne!(enc1, enc2);
}