use protontricks::config::Config;
use std::path::PathBuf;

#[test]
fn test_public_config_get_set() {
    let tmp_dir = tempfile::tempdir().unwrap();
    let custom_config = tmp_dir.path().join("someconfig");
    std::env::set_var("XDG_CONFIG_HOME", &custom_config);
    let mut conf = Config::new();
    let default_val = conf.get("publicsection", "optionnotset", "some_public_default");
    assert_eq!(default_val, "some_public_default");
    conf.set("publicsection", "publicopt", "vvvtest");
    assert_eq!(conf.get("publicsection", "publicopt", "bad"), "vvvtest");
    conf.set("publicsection", "publicopt", "publicvalue2");
    assert_eq!(conf.get("publicsection", "publicopt", "bad"), "publicvalue2");
    let config_path = custom_config.join("protontricks").join("config.ini");
    assert!(config_path.exists());
    let content = std::fs::read_to_string(&config_path).unwrap();
    assert!(content.contains("publicsection"));
    assert!(content.contains("publicopt"));
    assert!(content.contains("publicvalue2"));
}