// Public: Translated from public_tests/public_deye_active_power_regulation_test.py

#[test]
fn test_active_power_regulation_public() {
    let result = public_regulate_active_power(300.0, 200.0);
    assert_eq!(result, 200.0);
}

fn public_regulate_active_power(input: f64, target: f64) -> f64 {
    if input > target { target } else { input }
}