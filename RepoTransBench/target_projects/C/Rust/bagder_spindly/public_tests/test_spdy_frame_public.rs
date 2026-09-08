use bagder_spindly::sample_sum;

#[test]
fn test_sample_sum_values() {
    // Chosen different values for public test scenario
    assert_eq!(sample_sum(11, 29), 40);
    assert_eq!(sample_sum(-21, 20), -1);
    assert_eq!(sample_sum(100, -75), 25);
}