use mardix_flask_recaptcha::ReCaptcha;

#[test]
fn test_public_html_generation_different() {
    let mut recaptcha = ReCaptcha::new();
    recaptcha.site_key = "pub-key-test".to_string();
    let html = recaptcha.get_code();
    assert!(html.contains("pub-key-test"));
    assert!(html.contains("g-recaptcha"));
}

#[test]
fn test_public_theme_in_html() {
    let mut recaptcha = ReCaptcha::new();
    recaptcha.site_key = "test-key".to_string();
    recaptcha.theme = "dark".to_string();
    let html = recaptcha.get_code();
    assert!(html.contains("data-theme=\"dark\""));
}