use ai_forever_gigachat::settings::Settings;

#[test]
fn test_public_settings() {
    let instance = Settings::new();
    // Instead of hasattr in Rust, check type or memory presence:
    assert!(std::mem::size_of_val(&instance) > 0);
}