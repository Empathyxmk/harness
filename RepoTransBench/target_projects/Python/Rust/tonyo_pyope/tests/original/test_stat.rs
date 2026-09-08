use crate::stat::HGD;
use crate::ope::ValueRange;
use crate::stat::sample_uniform;

#[test]
fn test_uniform() {
    // Short ranges
    let value = 10;
    let unit_range = ValueRange::new(value, value);
    assert_eq!(sample_uniform(unit_range.clone(), vec![].into_iter()), value);

    let short_range = ValueRange::new(value, value + 1);
    assert_eq!(sample_uniform(short_range.clone(), vec![0].into_iter()), value);
    assert_eq!(sample_uniform(short_range.clone(), vec![1].into_iter()), value + 1);
    assert_eq!(sample_uniform(short_range.clone(), vec![0, 0, 1, 0, 0].into_iter()), value);

    // Should panic if no coins
    let res = std::panic::catch_unwind(|| {
        sample_uniform(short_range.clone(), vec![].into_iter());
    });
    assert!(res.is_err());

    // Medium ranges
    let start_range = 20;
    let end_range = start_range + 15;
    let range1 = ValueRange::new(start_range, end_range);
    assert_eq!(sample_uniform(range1.clone(), vec![0,0,0,0].into_iter()), start_range);
    assert_eq!(sample_uniform(range1.clone(), vec![0,0,0,1].into_iter()), start_range + 1);
    assert_eq!(sample_uniform(range1.clone(), vec![1,1,1,1].into_iter()), end_range);
    assert_eq!(sample_uniform(range1.clone(), std::iter::repeat(0).take(10)), start_range);

    // Negative range
    let start_range = -32;
    let end_range = -17;
    let range = ValueRange::new(start_range, end_range);
    assert_eq!(sample_uniform(range.clone(), std::iter::repeat(0).take(5)), start_range);
    assert_eq!(sample_uniform(range.clone(), std::iter::repeat(1).take(5)), end_range);

    // Mixed range
    let start_range = -32;
    let end_range = 31;
    let range = ValueRange::new(start_range, end_range);
    assert_eq!(sample_uniform(range.clone(), std::iter::repeat(0).take(6)), start_range);
    assert_eq!(sample_uniform(range, std::iter::repeat(1).take(6)), end_range);
}

#[test]
fn test_hypergeometric() {
    // Infinite random coins
    // Just use vector of zeros for deterministic
    assert_eq!(HGD::rhyper(5, 0, 5, vec![].into_iter()), 0);
    assert_eq!(HGD::rhyper(6, 6, 0, vec![].into_iter()), 6);
    assert_eq!(HGD::rhyper(1 << 32, 0, 1 << 32, vec![].into_iter()), 0);
    assert_eq!(HGD::rhyper(1 << 64, 1 << 64, 0, vec![].into_iter()), 1 << 64);
    assert_eq!(HGD::rhyper(1 << 32, 2, (1 << 32) - 2, vec![].into_iter()), 2);
}