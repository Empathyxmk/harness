use mardix_flask_recaptcha::{ReCaptcha, DEFAULTS};
use std::collections::HashMap;

#[test]
fn test_public_defaults_are_different() {
    assert_eq!(DEFAULTS.get("ssl_verify").unwrap(), "true");
    assert!(DEFAULTS.get("size").is_some());
}

#[test]
fn test_public_recaptcha_initial_config() {
    // We'll model config as a parameter set for Rust
    let options = HashMap::from([
        ("theme".to_string(), "light".to_string()),
        ("size".to_string(), "compact".to_string()),
    ]);
    let mut recaptcha = ReCaptcha::new();
    recaptcha.site_key = "publicUnique123".to_string();
    recaptcha.secret_key = "publicSecretABC".to_string();
    recaptcha.options = Some(options.clone());
    assert_eq!(recaptcha.site_key, "publicUnique123".to_string());
    assert_eq!(recaptcha.secret_key, "publicSecretABC".to_string());
    assert_eq!(recaptcha.options.as_ref().unwrap().get("theme").unwrap(), "light");
    assert_eq!(recaptcha.options.as_ref().unwrap().get("size").unwrap(), "compact");
}