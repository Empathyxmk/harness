// Translation of tests/unit/test_is_attacker.c
use std::sync::{Mutex, Once};
use lazy_static::lazy_static;

lazy_static! {
    static ref INIT_CALL_COUNT: Mutex<u32> = Mutex::new(0);
    static ref MOCK_ENV_VAL: Mutex<Option<&'static str>> = Mutex::new(None);
    static ref ATTACKER_STATE: Mutex<Option<i32>> = Mutex::new(None);
}

fn init() {
    let mut count = INIT_CALL_COUNT.lock().unwrap();
    *count += 1;
}

// Simulate environment lookup by using our test override
fn getenv(s: &str) -> Option<&'static str> {
    let env = MOCK_ENV_VAL.lock().unwrap();
    if let Some(val) = &*env {
        if s == "BEURK_ATK_ENV" {
            return Some(*val);
        }
    }
    None
}

// The function under test with simulated static caching
fn is_attacker() -> i32 {
    // In the C code, static int attacker = -1;
    // We'll use a lazy_static Mutex<Option<i32>>
    init();
    let mut attacker_ref = ATTACKER_STATE.lock().unwrap();
    if let Some(val) = *attacker_ref {
        return val;
    }
    let result =
        if getenv("BEURK_ATK_ENV").is_some() {
            1
        } else {
            0
        };
    *attacker_ref = Some(result);
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn attacker_path() {
        *MOCK_ENV_VAL.lock().unwrap() = Some("dummy");
        // Reset the static for repeatable test
        *ATTACKER_STATE.lock().unwrap() = None;

        let ret = is_attacker();
        assert_eq!(ret, 1);
        let ret2 = is_attacker();
        assert_eq!(ret2, 1); // static cache
    }

    #[test]
    fn non_attacker_path() {
        *MOCK_ENV_VAL.lock().unwrap() = None;
        *ATTACKER_STATE.lock().unwrap() = None;

        let ret = is_attacker();
        assert_eq!(ret, 0);
        let ret2 = is_attacker();
        assert_eq!(ret2, 0); // static cache
    }
}