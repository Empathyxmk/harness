// Public: Translated from public_tests/public_deye_multi_inverter_data_aggregator_test.py

#[test]
fn test_agg_public_sum() {
    let data = [5.0, 2.0, 1.0];
    let sum: f64 = data.iter().sum();
    assert_eq!(sum, 8.0);
}