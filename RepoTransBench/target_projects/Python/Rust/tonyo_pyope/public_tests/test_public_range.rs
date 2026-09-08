use crate::ope::ValueRange;

#[test]
fn test_range_size_public() {
    let r = ValueRange::new(-10, 20);
    assert_eq!(r.size(), 31);
}

#[test]
fn test_range_copy_public() {
    let r1 = ValueRange::new(100, 200);
    let r2 = r1.copy();
    assert_eq!(r1.start, r2.start);
    assert_eq!(r1.end, r2.end);
    assert_ne!((&r1 as *const _), (&r2 as *const _)); // Not same object
}

#[test]
fn test_range_contains_public() {
    let r = ValueRange::new(15, 25);
    assert!(r.contains(20));
    assert!(!r.contains(14));
    assert!(r.contains(25));
    assert!(!r.contains(26));
}

#[test]
fn test_range_repr_public() {
    let r = ValueRange::new(5, 10);
    assert!(format!("{:?}", r).contains("ValueRange"));
}