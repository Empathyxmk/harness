use maskerlogger::utils;
use std::env;

#[test]
fn test_get_config_file_path() {
    let path = utils::get_config_file_path(None);
    assert!(path.ends_with("gitleaks.toml"));
    assert!(path.to_string_lossy().contains("config"));
}

#[test]
fn test_get_config_file_path_custom() {
    let cfg = utils::get_config_file_path(Some("customfile.toml"));
    assert!(cfg.ends_with("customfile.toml"));
}