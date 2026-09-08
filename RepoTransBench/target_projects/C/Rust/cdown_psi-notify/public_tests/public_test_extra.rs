use psi_notify::*;

#[test]
fn test_streq_cases_public() {
    assert!(streq(Some("Public"), Some("Public")));
    assert!(!streq(Some("Public"), Some("Private")));
    assert!(strceq(Some("Public"), Some("PUBLic")));
    assert!(!strceq(Some("Public"), Some("Hidden")));
    assert!(!streq(Some("Public"), None));
    assert!(!strceq(None, Some("Public")));
}

#[test]
fn test_strceq_numbers_public() {
    assert!(strceq(Some("123abc"), Some("123ABC")));
    assert!(!strceq(Some("456def"), Some("654DEF")));
}

#[test]
fn test_strnull_edge_public() {
    assert_eq!(strnull(Some("notnull")), "notnull");
    assert_eq!(strnull(None), "");
}

#[test]
fn test_snprintf_overflow_public() {
    let mut buf = [0u8; 5];
    snprintf_check(&mut buf, "%s", "abcd");
    let s = std::str::from_utf8(&buf[..4]).unwrap();
    assert_eq!(s, "abcd");
    snprintf_check(&mut buf, "%s", "123456789");
    assert_eq!(buf[4], 0);
}

#[test]
fn test_parse_boolean_misc_public() {
    assert_eq!(parse_boolean(Some("YES")), 1);
    assert_eq!(parse_boolean(Some("No")), 0);
    assert_eq!(parse_boolean(Some("tRuE")), 1);
    assert_eq!(parse_boolean(Some("OFF")), 0);
    assert_eq!(parse_boolean(Some("maybeNo")), -1);
    assert_eq!(parse_boolean(None), -1);
}

#[test]
fn test_isnan_f_ltgt_public() {
    let nan_val = (-42.0f64).sqrt();
    assert!(isnan_f(nan_val));
    assert!(!isnan_f(-2.0));
}

#[test]
fn test_active_inactive_struct_public() {
    let a = Alert { value: 5 };
    assert_eq!(active_inactive(&a), "inactive");
}