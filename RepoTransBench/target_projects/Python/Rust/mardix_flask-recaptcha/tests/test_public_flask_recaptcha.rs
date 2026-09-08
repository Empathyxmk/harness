use mardix_flask_recaptcha::ReCaptcha;

#[test]
fn test_public_set_and_get_site_key() {
    let mut recaptcha = ReCaptcha::new();
    recaptcha.site_key = "different_public_key".to_string();
    assert_eq!(recaptcha.site_key, "different_public_key".to_string());
}

#[test]
fn test_public_set_and_get_secret_key() {
    let mut recaptcha = ReCaptcha::new();
    recaptcha.secret_key = "different_public_secret".to_string();
    assert_eq!(recaptcha.secret_key, "different_public_secret".to_string());
}

#[test]
fn test_public_language_setter_and_getter() {
    let mut recaptcha = ReCaptcha::new();
    recaptcha.language = "fr".to_string();
    assert_eq!(recaptcha.language, "fr".to_string());
}

#[test]
fn test_public_theme_setter_and_getter() {
    let mut recaptcha = ReCaptcha::new();
    recaptcha.theme = "dark".to_string();
    assert_eq!(recaptcha.theme, "dark".to_string());
}