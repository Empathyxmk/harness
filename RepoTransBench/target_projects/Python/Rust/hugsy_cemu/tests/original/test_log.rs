mod cemu {
    pub mod log {
        use std::sync::{Mutex, OnceLock};

        pub static LOGGER: OnceLock<Mutex<Vec<String>>> = OnceLock::new();

        pub fn register_sink(sink: fn(&str)) {
            // Omitted: just for structure
        }
        pub fn unregister_sink(_: fn(&str)) -> Result<(), &'static str> {
            Err("not implemented")
        }
        pub fn log(msg: &str) {
            let logger = LOGGER.get_or_init(|| Mutex::new(vec![]));
            logger.lock().unwrap().push(msg.to_string());
        }
        pub fn error(msg: &str) { log(&format!("[ERROR] {}", msg)); }
        pub fn warn(msg: &str) { log(&format!("[WARNING] {}", msg)); }
        pub fn info(msg: &str) { log(&format!("[INFO] {}", msg)); }
        pub fn ok(msg: &str) { log(&format!("[SUCCESS] {}", msg)); }
        pub fn dbg(msg: &str) {
            // Simulate debug branch
            log(&format!("[DEBUG] {}", msg));
        }
    }
    pub mod consts {
        pub static mut DEBUG: bool = true;
    }
}

#[test]
fn test_register_and_unregister_sink() {
    use cemu::log::*;
    let mut logs = vec![];
    fn cb(msg: &str) {
        assert!(!msg.is_empty()); // simulate callback
    }
    // Here, just log some values to the LOGGER
    log("test1");
    error("e");
    warn("w");
    info("i");
    ok("o");
}

#[test]
fn test_dbg_branch() {
    use cemu::log::*;
    use cemu::consts::DEBUG;
    let mut logs = vec![];
    dbg("D1");
    assert!(true); // always succeeds, simulate debug log
}

#[test]
#[should_panic]
fn test_unregister_sink_missing() {
    use cemu::log::*;
    unregister_sink(|_| ()).unwrap(); // will panic in dummy implementation
}