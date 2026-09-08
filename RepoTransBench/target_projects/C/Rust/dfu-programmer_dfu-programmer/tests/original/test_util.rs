use dfu_programmer::util::{dfu_debug, dfu_debug_int};
use std::sync::Once;

static INIT: Once = Once::new();

// Setup function to initialize any test dependencies
fn initialize() {
    INIT.call_once(|| {
        // Set global debug level
        unsafe {
            dfu_programmer::util::DEBUG = 100;
        }
    });
}

#[test]
fn test_dfu_debug_level_high() {
    initialize();
    // This message should not print, because debug == 100, level=150
    dfu_debug_int("testfile", "testfunc", 42, 150, "should not print", 123);
    // No direct assertion, we're just making sure it doesn't crash
    assert!(true);
}

#[test]
fn test_dfu_debug_level_low() {
    initialize();
    // This message should print, because debug == 100, level=50
    dfu_debug("testfile", "testfunc", 42, 50, "message", "low-level debug");
    // No direct assertion, we're just making sure it doesn't crash
    assert!(true);
}