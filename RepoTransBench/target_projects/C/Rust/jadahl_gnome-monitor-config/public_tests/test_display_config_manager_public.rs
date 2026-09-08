#[test]
fn test_public_new_manager() {
    // Test that a new manager object is alloc'd and initialized
    let mgr = crate::display_config_manager::DisplayConfigManager::new();
    assert!(mgr.is_some());
    assert!(mgr.unwrap().is_initialized());
}

#[test]
fn test_public_null_manager() {
    // Test that is_initialized returns false for NULL pointer
    let null_mgr: Option<&crate::display_config_manager::DisplayConfigManager> = None;
    assert_eq!(crate::display_config_manager::is_initialized_from_option(null_mgr), false);
}

#[test]
fn test_public_free_manager() {
    // In Rust, memory is automatically freed when values go out of scope
    // This test ensures we can create and drop a manager without issues
    let mgr = crate::display_config_manager::DisplayConfigManager::new();
    assert!(mgr.is_some());
    
    // Explicit drop is not necessary in Rust but included to match C test's logic
    drop(mgr);
}

#[test]
fn test_public_free_null_manager() {
    // Test that dropping a None value doesn't crash
    let null_mgr: Option<crate::display_config_manager::DisplayConfigManager> = None;
    drop(null_mgr); // This should not panic
}