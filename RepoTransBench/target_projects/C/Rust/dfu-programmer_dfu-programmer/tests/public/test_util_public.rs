use dfu_programmer::util::{min, max, clamp};

#[test]
fn test_min_different_values() {
    let a = 10;
    let b = 8;
    assert_eq!(min(a, b), 8);
    assert_eq!(min(b, a), 8);
    assert_eq!(min(-10, 10), -10);
}

#[test]
fn test_max_different_values() {
    let a = -15;
    let b = 4;
    assert_eq!(max(a, b), 4);
    assert_eq!(max(b, a), 4);
    assert_eq!(max(-20, -7), -7);
}

#[test]
fn test_clamp_different_cases() {
    assert_eq!(clamp(7, 3, 9), 7);      // inside
    assert_eq!(clamp(-5, 0, 12), 0);    // below
    assert_eq!(clamp(30, 6, 26), 26);   // above
    assert_eq!(clamp(6, 6, 6), 6);      // all equal
    assert_eq!(clamp(17, 12, 16), 16);  // just above
    assert_eq!(clamp(11, 12, 16), 12);  // just below
}