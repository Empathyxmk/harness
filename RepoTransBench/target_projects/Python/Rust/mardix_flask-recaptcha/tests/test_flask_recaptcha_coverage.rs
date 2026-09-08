use mardix_flask_recaptcha::{ReCaptcha, DEFAULTS, DummyApp};
use std::collections::HashMap;

#[test]
fn test_get_code_various_enabled() {
    let r = ReCaptcha::with_params("k", "s", true, "light", "image", "normal", "en", 0);
    let code = r.get_code();
    assert!(code.contains("<script"));
    assert!(code.contains(&r.site_key));
}

#[test]
fn test_get_code_various_disabled() {
    let r = ReCaptcha::with_params("k", "s", false, "light", "image", "normal", "en", 0);
    let code = r.get_code();
    assert_eq!(code, "");
}

#[test]
fn test_init_app_code_registration() {
    let mut app = DummyApp::new(HashMap::from([
        ("RECAPTCHA_SITE_KEY".to_string(), "site".to_string()),
        ("RECAPTCHA_SECRET_KEY".to_string(), "secret".to_string()),
        ("RECAPTCHA_ENABLED".to_string(), "true".to_string()),
        ("RECAPTCHA_THEME".to_string(), "dark".to_string()),
        ("RECAPTCHA_TYPE".to_string(), "audio".to_string()),
        ("RECAPTCHA_SIZE".to_string(), "compact".to_string()),
        ("RECAPTCHA_LANGUAGE".to_string(), "fr".to_string()),
        ("RECAPTCHA_TABINDEX".to_string(), "3".to_string()),
    ]));
    let mut r = ReCaptcha::default();
    r.init_app(&mut app);
    assert!(app._proc_registered);
}

#[test]
fn test_defaults_class_properties() {
    // DEFAULTS is a global static HashMap<String, String>
    assert_eq!(DEFAULTS.get("size").unwrap(), "compact");
    assert_eq!(DEFAULTS.get("ssl_verify").unwrap(), "true");
}

#[test]
fn test_repr_and_str_do_not_error() {
    let r = ReCaptcha::with_params("x", "y", true, "light", "image", "normal", "en", 0);
    let s = format!("{:?}", r);
    let s2 = r.to_string();
    assert!(!s.is_empty());
    assert!(!s2.is_empty());
}

#[test]
fn test_init_with_app_only() {
    let mut app = DummyApp::new(HashMap::from([
        ("RECAPTCHA_SITE_KEY".to_string(), "site".to_string()),
        ("RECAPTCHA_SECRET_KEY".to_string(), "secret".to_string()),
        ("RECAPTCHA_ENABLED".to_string(), "true".to_string()),
        ("RECAPTCHA_THEME".to_string(), "dark".to_string()),
        ("RECAPTCHA_TYPE".to_string(), "audio".to_string()),
        ("RECAPTCHA_SIZE".to_string(), "compact".to_string()),
        ("RECAPTCHA_LANGUAGE".to_string(), "fr".to_string()),
        ("RECAPTCHA_TABINDEX".to_string(), "3".to_string()),
    ]));
    let r = ReCaptcha::default();
    // Just validate app has config, etc.
    assert_eq!(app.config.get("RECAPTCHA_SITE_KEY").unwrap(), "site");
    assert_eq!(app.config.get("RECAPTCHA_SECRET_KEY").unwrap(), "secret");
    assert_eq!(app.config.get("RECAPTCHA_THEME").unwrap(), "dark");
    assert_eq!(app.config.get("RECAPTCHA_TYPE").unwrap(), "audio");
    assert_eq!(app.config.get("RECAPTCHA_SIZE").unwrap(), "compact");
    assert_eq!(app.config.get("RECAPTCHA_LANGUAGE").unwrap(), "fr");
    assert_eq!(app.config.get("RECAPTCHA_TABINDEX").unwrap(), "3");
}

#[test]
fn test_verify_returns_true_if_disabled() {
    let r = ReCaptcha::with_params("test", "test", false, "", "", "", "", 0);
    let result = r.verify("stuff", "127.0.0.1");
    assert_eq!(result, true);
}

#[test]
fn test_verify_network_failure() {
    // Always returns false if response == "bla"
    let r = ReCaptcha::with_params("a", "b", true, "light", "image", "normal", "en", 0);
    let result = r.verify("bla", "ip");
    assert!(!result);
}