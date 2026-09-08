use crate::config::Config;
use std::path::PathBuf;

#[test]
fn test_config_with_missing_file() {
    let p = PathBuf::from("notexisting.toml");
    let config = Config::with_path(p.clone());
    assert_eq!(config.path, p);
}

#[test]
fn test_config_fallback_default() {
    let p = PathBuf::from("notexisting2.toml");
    let config = Config::with_path(p.clone());
    assert_eq!(config.path, p);
    assert_eq!(config.runner, "pytest".to_string());
    assert_eq!(config.delay, 0.2);
}