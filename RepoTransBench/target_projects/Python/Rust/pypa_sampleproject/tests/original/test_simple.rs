use pypa_sampleproject::simple::add_one;

#[test]
fn test_add_one_positive() {
    assert_eq!(add_one(2), 3);
}

#[test]
fn test_add_one_zero() {
    assert_eq!(add_one(0), 1);
}

#[test]
fn test_add_one_negative() {
    assert_eq!(add_one(-5), -4);
}

#[test]
fn test_add_one_float() {
    assert_eq!(add_one(2.5_f64), 3.5_f64);
}

#[test]
#[should_panic(expected = "TypeError: add_one() argument must be a number")]
fn test_add_one_str_raises() {
    let _ = add_one("hi");
}