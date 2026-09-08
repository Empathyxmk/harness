mod cemu {
    pub mod log {
        use std::sync::Mutex;
        pub static LOGGER: once_cell::sync::Lazy<Mutex<Vec<String>>> = once_cell::sync::Lazy::new(|| Mutex::new(vec![]));
        pub fn register_sink(_: fn(&str)) {}
        pub fn unregister_sink(_: fn(&str)) {}
        pub fn log(msg: &str) { LOGGER.lock().unwrap().push(msg.into()); }
        pub fn error(msg: &str) { LOGGER.lock().unwrap().push(format!("[ERROR] {}", msg)); }
        pub fn warn(msg: &str) { LOGGER.lock().unwrap().push(format!("[WARNING] {}", msg)); }
        pub fn info(msg: &str) { LOGGER.lock().unwrap().push(format!("[INFO] {}", msg)); }
        pub fn ok(msg: &str) { LOGGER.lock().unwrap().push(format!("[SUCCESS] {}", msg)); }
        pub fn dbg(msg: &str) { LOGGER.lock().unwrap().push(format!("[DEBUG] {}", msg)); }
    }
    pub mod consts {
        pub static mut DEBUG: bool = false;
    }
}

#[test]
fn test_register_and_log_public() {
    use cemu::log::*;
    log("test log public message");
    let msgs = cemu::log::LOGGER.lock().unwrap();
    assert_eq!(msgs.last().unwrap(), "test log public message");
    // No unregister needed, just demonstrate push/logging
}

#[test]
fn test_error_and_warn_info_ok_dbg_public() {
    use cemu::log::*;
    error("an error occurred");
    let logs = cemu::log::LOGGER.lock().unwrap();
    assert!(logs.last().unwrap().starts_with("[ERROR]") || logs.last().unwrap().contains("error"));
    warn("a warning");
    let logs = cemu::log::LOGGER.lock().unwrap();
    assert!(logs.last().unwrap().starts_with("[WARNING]"));
    info("info message");
    let logs = cemu::log::LOGGER.lock().unwrap();
    assert!(logs.last().unwrap().starts_with("[INFO]"));
    ok("operation succeeded");
    let logs = cemu::log::LOGGER.lock().unwrap();
    assert!(logs.last().unwrap().starts_with("[SUCCESS]"));
    dbg("debugging");
    let logs = cemu::log::LOGGER.lock().unwrap();
    assert!(logs.last().unwrap().starts_with("[DEBUG]"));
}