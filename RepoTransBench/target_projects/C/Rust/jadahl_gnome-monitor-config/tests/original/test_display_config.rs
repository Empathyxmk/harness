#[test]
fn test_new_config() {
    // Test that a new config object is alloc'd and id is set to 42
    let cfg = crate::display_config::DisplayConfig::new();
    assert!(cfg.is_some());
    assert_eq!(cfg.unwrap().get_id(), 42);
}

#[test]
fn test_null_config() {
    // Test that get_id returns -1 for NULL pointer
    let null_cfg: Option<&crate::display_config::DisplayConfig> = None;
    assert_eq!(crate::display_config::get_id_from_option(null_cfg), -1);
}

#[test]
fn test_free_config() {
    // In Rust, memory is automatically freed when values go out of scope
    // This test ensures we can create and drop a configuration without issues
    let cfg = crate::display_config::DisplayConfig::new();
    assert!(cfg.is_some());
    
    // Explicit drop is not necessary in Rust but included to match C test's logic
    drop(cfg);
}

#[test]
fn test_free_null() {
    // Test that dropping a None value doesn't crash
    let null_cfg: Option<crate::display_config::DisplayConfig> = None;
    drop(null_cfg); // This should not panic
}