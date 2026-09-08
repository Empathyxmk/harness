use ai_forever_gigachat::settings::Settings;

#[test]
fn test_settings() {
    let settings = Settings::new();
    assert!(std::mem::size_of_val(&settings) > 0);
}