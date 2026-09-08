use psi_notify::*;

#[test]
fn test_streq_cases() {
    assert!(streq(Some("bar"), Some("bar")));
    assert!(!streq(Some("foo"), Some("baz")));
}

#[test]
fn test_strceq_cases() {
    assert!(strceq(Some("ABC"), Some("abc")));
    assert!(!strceq(Some("abc"), Some("abcd")));
    assert!(!strceq(Some("test"), None));
    assert!(!strceq(None, Some("test")));
}

#[test]
fn test_parse_boolean_varied() {
    assert_eq!(parse_boolean(Some("false")), 0);
    assert_eq!(parse_boolean(Some("on")), 1);
    assert_eq!(parse_boolean(Some("off")), 0);
    assert_eq!(parse_boolean(Some("dummy")), -1);
    assert_eq!(parse_boolean(Some("")), -1);
}

#[test]
fn test_snprintf_check_bounds() {
    let mut buf = [0u8; 4];
    snprintf_check(&mut buf, "%s", "12345");
    assert_eq!(buf[3], 0);
}

#[test]
fn test_isnan_f_nan0() {
    assert!(isnan_f(f64::NAN));
}