use psi_notify::*;

#[test]
fn test_streq_strceq() {
    assert!(streq(Some("foo"), Some("foo")));
    assert!(!streq(Some("foo"), Some("bar")));
    assert!(strceq(Some("foo"), Some("FOO")));
    assert!(!strceq(Some("foo"), Some("bar")));
    assert!(!streq(None, Some("foo")));
    assert!(!strceq(None, Some("foo")));
    assert!(!streq(Some("foo"), None));
    assert!(!strceq(Some("foo"), None));
}

#[test]
fn test_strnull() {
    assert_eq!(strnull(Some("abc")), "abc");
    assert_eq!(strnull(None), "");
}

#[test]
fn test_snprintf_check() {
    let mut buf = [0u8; 8];
    snprintf_check(&mut buf, "%s", "abcdefg");
    let s = std::str::from_utf8(&buf[..7]).unwrap();
    assert_eq!(s, "abcdefg");
    snprintf_check(&mut buf, "%s", "abcdefghij");
    assert_eq!(buf[7], 0);
}

#[test]
fn test_parse_boolean() {
    assert_eq!(parse_boolean(Some("yes")), 1);
    assert_eq!(parse_boolean(Some("YES")), 1);
    assert_eq!(parse_boolean(Some("1")), 1);
    assert_eq!(parse_boolean(Some("true")), 1);
    assert_eq!(parse_boolean(Some("on")), 1);
    assert_eq!(parse_boolean(Some("no")), 0);
    assert_eq!(parse_boolean(Some("off")), 0);
    assert_eq!(parse_boolean(Some("FALSE")), 0);
    assert_eq!(parse_boolean(Some("0")), 0);
    assert_eq!(parse_boolean(Some("maybe")), -1);
    assert_eq!(parse_boolean(None), -1);
}

#[test]
fn test_isnan_f() {
    assert!(isnan_f(f64::NAN));
    assert!(!isnan_f(1.0));
}

#[test]
fn test_active_inactive() {
    let a = Alert::default();
    assert_eq!(active_inactive(&a), "inactive");
}