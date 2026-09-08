use maskerlogger::utils;

#[test]
fn test_get_config_file_path_non_default() {
    let path = utils::get_config_file_path(Some("alternative_config.toml"));
    assert!(path.ends_with("alternative_config.toml"));
}

#[test]
fn test_get_config_file_path_contains_maskerlogger() {
    let path = utils::get_config_file_path(None);
    assert!(path.to_string_lossy().contains("maskerlogger"));
}