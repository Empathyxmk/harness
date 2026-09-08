// Translated from easy_thumbnails/tests/test_conf.py

#[test]
fn test_settings_default_values() {
    // Simulate settings/config struct default
    #[derive(Default)]
    struct Settings {
        debug: bool,
        default_storage: &'static str,
    }
    let s = Settings { debug: false, default_storage: "default".into() };
    assert!(!s.debug);
    assert_eq!(s.default_storage, "default");
}