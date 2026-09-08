//! Rust translation of source/Test/test_dht_read_public.c
//! Simple public test with value assertions.

#[test]
fn test_public_dummy_humidity_temp() {
    let humidity = 60.5f32;
    let temperature = 36.6f32;
    assert!((humidity - 60.5).abs() < 0.001);
    assert!((temperature - 36.6).abs() < 0.001);
    println!("Public Test passed: humidity={:.1} temp={:.1}", humidity, temperature);
}