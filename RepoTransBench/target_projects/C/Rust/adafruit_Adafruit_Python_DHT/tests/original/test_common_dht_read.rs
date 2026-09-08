//! Rust translation of source/Test/test_common_dht_read.c
//! Original logic test for DHT reading, using stub algorithm.

use adafruit_dht_rust::read_dht_data_orig;

#[test]
fn test_dht_read_returns_success() {
    let result = read_dht_data_orig(11, 2);
    match result {
        Ok((humidity, temp)) => {
            assert!((humidity - 43.0).abs() < 0.001, "Expected humidity 43.0, got {}", humidity);
            assert!((temp - 32.0).abs() < 0.001, "Expected temperature 32.0, got {}", temp);
        }
        Err(e) => panic!("Expected Ok, got error code: {}", e),
    }
}

#[test]
fn test_dht_read_returns_data_error() {
    let result = read_dht_data_orig(22, 10);
    assert!(matches!(result, Err(-2)), "Expected error code -2, got {:?}", result);
}

#[test]
fn test_dht_read_returns_timeout() {
    let result = read_dht_data_orig(0, 0);
    assert!(matches!(result, Err(-1)), "Expected error code -1, got {:?}", result);
}