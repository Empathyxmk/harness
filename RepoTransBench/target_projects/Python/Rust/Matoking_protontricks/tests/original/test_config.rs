use protontricks::config::{get_config};

#[test]
fn test_config() {
    let home_dir = std::env::var("HOME").unwrap_or_else(|_| ".".to_string());
    let mut config = get_config();
    config.set("General", "test_field", "test_value");
    // Check config file existence.
    let config_path = std::path::Path::new(&home_dir)
        .join(".config/protontricks/config.ini");
    // The test expects file write as a side effect.
    assert!(config_path.exists());
    let content = std::fs::read_to_string(&config_path).unwrap_or_default();
    assert!(content.contains("test_value"));
    let config_2 = get_config();
    assert_eq!(
        config_2.get("General", "test_field", "bad"),
        "test_value"
    );
}

#[test]
fn test_config_default() {
    let config = get_config();
    assert_eq!(
        config.get("General", "fake_field", "default_value"),
        "default_value"
    );
}