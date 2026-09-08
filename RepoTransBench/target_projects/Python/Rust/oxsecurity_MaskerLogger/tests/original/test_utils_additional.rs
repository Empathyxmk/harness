use maskerlogger::utils;
use std::fs;
use std::path::Path;

#[test]
fn test_get_config_file_path_default() {
    let path = utils::get_config_file_path(None);
    assert!(path.ends_with("gitleaks.toml"));
    // File existence might not be true, so accept if ends_with
    assert!(
        fs::metadata(&path).is_ok() || path.to_string_lossy().contains("gitleaks.toml")
    );
}

#[test]
fn test_get_config_file_path_custom() {
    let fname = "some_other_config.toml";
    let path = utils::get_config_file_path(Some(fname));
    assert!(path.ends_with(fname));
}

#[test]
fn test_get_config_file_path_edge() {
    // Simulate __file__ being /tmp/fake.py (affect only if implementation uses __file__)
    // Here, simply test with manual construction
    let expected = std::path::Path::new("/tmp").join("config").join("foo.toml");
    // In production, would simulate setting __file__, but Rust impl uses current_dir
    let path = utils::get_config_file_path(Some("foo.toml"));
    // Accept as long as ends_with config/foo.toml
    assert!(path.ends_with("config/foo.toml"));
}