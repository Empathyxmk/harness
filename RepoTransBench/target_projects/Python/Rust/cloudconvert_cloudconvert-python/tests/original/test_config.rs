use cloudconvert_cloudconvert_rust::config;

#[test]
fn test_config_defaults() {
    let cfg = config::Config::default();
    assert_eq!(cfg.api_key, None);
    assert_eq!(cfg.sandbox, false);
}

#[test]
fn test_config_set_api_key() {
    let mut cfg = config::Config::default();
    cfg.set_api_key("abc123".to_string());
    assert_eq!(cfg.api_key.as_deref(), Some("abc123"));
}

#[test]
fn test_config_enable_sandbox() {
    let mut cfg = config::Config::default();
    cfg.set_sandbox(true);
    assert_eq!(cfg.sandbox, true);
}