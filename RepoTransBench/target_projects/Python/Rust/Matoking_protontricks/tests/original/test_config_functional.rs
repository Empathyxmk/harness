use protontricks::config::{Config, get_config};
use std::path::PathBuf;

#[test]
fn test_config_get_set() {
    let tmp_dir = tempfile::tempdir().unwrap();
    let test_conf_dir = tmp_dir.path().join("myconf");
    std::fs::create_dir(&test_conf_dir).unwrap();
    std::env::set_var("XDG_CONFIG_HOME", &test_conf_dir);
    let config_file = test_conf_dir.join("protontricks").join("config.ini");
    if config_file.exists() {
        std::fs::remove_file(&config_file).unwrap();
    }
    let mut conf = Config::new();
    assert_eq!(conf.get("section", "option", "123"), "123");
    conf.set("section", "option", "xyz");
    assert_eq!(conf.get("section", "option", "0"), "xyz");
    assert!(config_file.exists());
    let conf2 = Config::new();
    assert_eq!(conf2.get("section", "option", "0"), "xyz");
}

#[test]
fn test_config_file_not_found() {
    let tmp_dir = tempfile::tempdir().unwrap();
    std::env::set_var("XDG_CONFIG_HOME", tmp_dir.path());
    let config_file = tmp_dir.path().join("protontricks").join("config.ini");
    if config_file.exists() {
        std::fs::remove_file(&config_file).unwrap();
    }
    let conf = Config::new();
    assert_eq!(conf.get("missing", "x", ""), "");
}

#[test]
fn test_config_default_value() {
    let tmp_dir = tempfile::tempdir().unwrap();
    std::env::set_var("XDG_CONFIG_HOME", tmp_dir.path());
    let mut conf = Config::new();
    conf.set("sec", "opt", "val");
    assert_eq!(conf.get("sec", "opt", "no"), "val");
    assert_eq!(conf.get("sec", "noopt", "def"), "def");
}

#[test]
fn test_get_config_returns_config() {
    let _ = get_config();
}