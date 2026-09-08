// Translation of uuslug/tests/public_test_apps_py.py to Rust

use crate::apps::UuslugConfig;

#[test]
fn test_apps_config_name_public() {
    let app_config = UuslugConfig::new("uuslug", "uuslug");
    assert_eq!(app_config.name, "uuslug");
    assert!(app_config.verbose_name.to_lowercase().contains("uuslug"));
}