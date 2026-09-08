use crate::ope::{ValueRange};
use crate::errors::InvalidRangeLimitsError;

#[test]
fn test_range_simple() {
    let start = 2;
    let end = 1000;
    let r = ValueRange::new(start, end);
    assert_eq!(r.size(), 999);
    for i in start..=end {
        assert!(r.contains(i));
    }
    assert!(!r.contains(start - 1));
    assert!(!r.contains(end + 1));
    assert_eq!(r.range_bit_size(), 10);
}

#[test]
fn test_range_repr() {
    let a = ValueRange::new(1, 10);
    assert_eq!(format!("{:?}", a).contains("ValueRange"), true);
}

#[test]
fn test_invalid_range_ends() {
    let res = std::panic::catch_unwind(|| {
        ValueRange::new("123".parse().unwrap_or(0), 0);
    });
    assert!(res.is_err());

    let res = std::panic::catch_unwind(|| {
        ValueRange::new(0, "123".parse().unwrap_or(0));
    });
    assert!(res.is_err());

    let res = std::panic::catch_unwind(|| {
        ValueRange::new("123".parse().unwrap_or(0), "abc".parse().unwrap_or(0));
    });
    assert!(res.is_err());
}