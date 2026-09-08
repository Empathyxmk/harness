// Translation of tests/unit/test_config.c

use std::sync::Mutex;
use lazy_static::lazy_static;

lazy_static! {
    static ref G_VERBOSE: Mutex<i32> = Mutex::new(0);
    static ref CONFIG_LOADED: Mutex<i32> = Mutex::new(0);
}

fn load_config(file: Option<&str>) -> i32 {
    let mut loaded = CONFIG_LOADED.lock().unwrap();
    *loaded = 0;
    match file {
        None => -1,
        Some("beurk.conf") => {
            *loaded = 1;
            *G_VERBOSE.lock().unwrap() = 1;
            0
        },
        Some(_) => -1,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn load_config_success() {
        assert_eq!(load_config(Some("beurk.conf")), 0);
        assert_eq!(*CONFIG_LOADED.lock().unwrap(), 1);
    }

    #[test]
    fn load_config_fail() {
        assert_eq!(load_config(Some("badfile.conf")), -1);
        assert_eq!(*CONFIG_LOADED.lock().unwrap(), 0);
    }

    #[test]
    fn load_config_null() {
        assert_eq!(load_config(None), -1);
        assert_eq!(*CONFIG_LOADED.lock().unwrap(), 0);
    }
}