//! Rust translation of source/Test/test_dht_read.c
//! Very simple assertion/dummy test.

#[test]
fn test_dummy_humidity_temp() {
    let humidity = 50.0f32;
    let temperature = 42.0f32;
    assert!((humidity - 50.0).abs() < 0.001);
    assert!((temperature - 42.0).abs() < 0.001);
    println!("Test passed: humidity={:.1} temp={:.1}", humidity, temperature);
}