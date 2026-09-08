use najoshi_sickle::sliding::sliding_quality;

#[test]
fn test_sliding_quality_public() {
    let scores1 = [38, 40, 42, 46, 39];
    assert_eq!(sliding_quality(&scores1, 5, 3), 9);

    let scores2 = [33, 35, 37, 34, 33];
    assert_eq!(sliding_quality(&scores2, 5, 2), 4);

    let scores3 = [60, 65, 70, 75];
    assert_eq!(sliding_quality(&scores3, 4, 3), 4);

    let scores4 = [90, 80, 85];
    assert_eq!(sliding_quality(&scores4, 3, 2), 5);

    let scores5 = [100, 105, 110, 95, 90];
    assert_eq!(sliding_quality(&scores5, 5, 4), 8);
}