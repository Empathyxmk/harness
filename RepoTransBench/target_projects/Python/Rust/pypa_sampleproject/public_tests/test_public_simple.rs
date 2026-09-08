use pypa_sampleproject::simple::add_one;

#[test]
fn test_add_one_large_positive() {
    assert_eq!(add_one(100), 101);
}

#[test]
fn test_add_one_negative_one() {
    assert_eq!(add_one(-1), 0);
}

#[test]
fn test_add_one_large_negative() {
    assert_eq!(add_one(-99), -98);
}

#[test]
fn test_add_one_float_negative() {
    assert_eq!(add_one(-2.25_f64), -1.25_f64);
}

#[test]
#[should_panic(expected = "TypeError: add_one() argument must be a number")]
fn test_add_one_none_raises() {
    // Use Option type to simulate 'None'
    let _ = add_one::<Option<i32>>(None);
}