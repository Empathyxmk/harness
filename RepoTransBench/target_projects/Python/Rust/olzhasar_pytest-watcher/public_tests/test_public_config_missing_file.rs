use crate::config::Config;
use std::path::PathBuf;

#[test]
fn test_config_file_not_existent() {
    let conf = Config::with_path(PathBuf::from("surely_nonexistent_toml.toml"));
    assert_eq!(conf.path.file_name().unwrap().to_str().unwrap(), "surely_nonexistent_toml.toml");
    let loaded = conf.load();
    assert!(loaded.is_err());
}