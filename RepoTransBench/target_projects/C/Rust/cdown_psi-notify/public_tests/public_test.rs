use psi_notify::*;

#[test]
fn test_max_public() {
    assert_eq!(max(100, 50), 100);
    assert_eq!(max(-23, -22), -22);
    assert_eq!(max(0, 1), 1);
}

#[test]
fn test_min_public() {
    assert_eq!(min(53, 99), 53);
    assert_eq!(min(-10, -100), -100);
    assert_eq!(min(0, 0), 0);
}

#[test]
fn test_strempty_public() {
    assert!(strempty(Some("")));
    assert!(!strempty(Some("psi-notify")));
    assert!(strempty(None));
}

#[test]
fn test_streq_diff_public() {
    assert!(streq(Some("foo"), Some("foo")));
    assert!(streq(Some("BAR"), Some("BAR")));
    assert!(!streq(Some("foo"), Some("bar")));
    assert!(!streq(Some("baz"), Some("bax")));
    assert!(!streq(Some("baz"), None));
    assert!(!streq(None, Some("baz")));
}

#[test]
fn test_strceq_misc_public() {
    assert!(strceq(Some("HelLo"), Some("hello")));
    assert!(strceq(Some("TEST"), Some("test")));
    assert!(!strceq(Some("hello"), Some("world")));
    assert!(!strceq(Some("foO"), None));
    assert!(!strceq(None, Some("Bar")));
}

#[test]
fn test_parse_boolean_public() {
    assert_eq!(parse_boolean(Some("TRUE")), 1);
    assert_eq!(parse_boolean(Some("False")), 0);
    assert_eq!(parse_boolean(Some("on")), 1);
    assert_eq!(parse_boolean(Some("ofF")), 0);
    assert_eq!(parse_boolean(Some("perhaps")), -1);
    assert_eq!(parse_boolean(Some("")), -1);
    assert_eq!(parse_boolean(None), -1);
}