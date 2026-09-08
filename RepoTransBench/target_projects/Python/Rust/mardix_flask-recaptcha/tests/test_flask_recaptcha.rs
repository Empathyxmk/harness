use mardix_flask_recaptcha::ReCaptcha;

#[test]
fn test_init_with_default_args() {
    let r = ReCaptcha::new();
    // Rust: always has is_enabled as field
    assert!(r.is_enabled);
}

#[test]
fn test_site_key_and_secret_key() {
    let r = ReCaptcha::with_params("abc", "def", true, "light", "image", "normal", "en", 0);
    assert_eq!(r.site_key, "abc");
    assert_eq!(r.secret_key, "def");
}

#[test]
fn test_theme_and_type_property() {
    let r = ReCaptcha::default();
    assert!(!r.theme.is_empty());
    assert!(!r.type_.is_empty());
}

#[test]
fn test_set_params_method_exists() {
    let mut r = ReCaptcha::default();
    r.set_params(&[("a", 1), ("b", 2)]);
    assert_eq!(r.param["a"], 1);
    assert_eq!(r.param["b"], 2);
}

#[test]
fn test_validate_success() {
    let r = ReCaptcha::with_params("a", "b", true, "light", "image", "normal", "en", 0);
    let result = r.verify("SOME", "HOST");
    assert!(result);
}

#[test]
fn test_validate_fail() {
    let r = ReCaptcha::with_params("a", "b", true, "light", "image", "normal", "en", 0);
    let result = r.verify("FAIL", "HOST");
    assert!(!result);
}

#[test]
#[should_panic(expected = "fail")]
fn test_verify_exception() {
    let r = ReCaptcha::with_params("a", "b", true, "light", "image", "normal", "en", 0);
    r.verify("ANY", "FAILHOST");
}

#[test]
fn test_disabled_by_flag() {
    let r = ReCaptcha::with_params("", "", false, "", "", "", "", 0);
    let result = r.verify("ANY", "X");
    assert!(result);
}

#[test]
fn test_repr_and_str() {
    let r = ReCaptcha::with_params("public", "topsecret", true, "light", "image", "normal", "en", 0);
    assert!(format!("{:?}", r).contains("site_key"));
    assert!(!r.to_string().is_empty());
}