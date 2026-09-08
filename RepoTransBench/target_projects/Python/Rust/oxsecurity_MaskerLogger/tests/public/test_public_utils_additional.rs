use maskerlogger::utils;

#[test]
fn test_get_config_file_path_other_custom() {
    let cfg = utils::get_config_file_path(Some("anotherpublic.toml"));
    assert!(cfg.ends_with("anotherpublic.toml"));
}

#[test]
fn test_get_config_file_path_folder_check() {
    let cfg = utils::get_config_file_path(None);
    assert!(cfg.to_string_lossy().contains("config") || cfg.to_string_lossy().replace('\\', "/").contains("config"));
}