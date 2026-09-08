// Public: Translated from public_tests/public_deye_sensor_test.py

#[test]
fn test_sensor_public_scale() {
    assert_eq!(sensor_public_mul(2.0, 5.0), 10.0);
}

fn sensor_public_mul(a: f64, b: f64) -> f64 { a * b }