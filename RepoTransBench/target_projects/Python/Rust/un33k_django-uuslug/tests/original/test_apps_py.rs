// Translation of uuslug/tests/test_apps_py.py to Rust

use crate::apps;

#[test]
fn test_apps_module_import() {
    // At least one config symbol exists
    let _ = apps::AppConfig("uuslug".into(), "uuslug".into());
}

#[test]
fn test_apps_module_smoke() {
    let config = apps::AppConfig("uuslug".into(), "uuslug".into());
    // There is a doc-like symbol (label); always true in this stub
    assert!(config.label().len() > 0);
}