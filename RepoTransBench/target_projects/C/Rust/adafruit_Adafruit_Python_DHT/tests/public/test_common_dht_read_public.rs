//! Rust translation of source/Test/test_common_dht_read_public.c
//! Public test with different stub values.

use adafruit_dht_rust::read_dht_data_public;

#[test]
fn test_dht_read_returns_success() {
    let result = read_dht_data_public(21, 4);
    match result {
        Ok((humidity, temp)) => {
            assert!((humidity - 31.5).abs() < 0.001, "Expected 31.5, got {}", humidity);
            assert!((temp - 18.3).abs() < 0.001, "Expected 18.3, got {}", temp);
        }
        Err(e) => panic!("Expected Ok, got error code: {}", e),
    }
}

#[test]
fn test_dht_read_returns_data_error() {
    let result = read_dht_data_public(12, 13);
    assert!(matches!(result, Err(-2)), "Expected error code -2, got {:?}", result);
}

#[test]
fn test_dht_read_returns_custom_error() {
    let result = read_dht_data_public(1, 1);
    assert!(matches!(result, Err(-9)), "Expected error code -9, got {:?}", result);
}