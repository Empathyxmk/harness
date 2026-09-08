// Translation of tests/unit/test_is_hidden_file.c
use std::sync::Mutex;
use lazy_static::lazy_static;

const MAGIC_STRING: &str = "MAGIC";
const LIBRARY_NAME: &str = "libbeurk.so";
const PROC_PATH: &str = "/proc/";
const _STAT_VER: i32 = 0;
const MAX_LEN: usize = 128;
const ENV_LINE: &str = "{}/environ";
const HIDDEN_ENV_VAR: &str = "BEURK_ATK_ENV";

// global stat/envfile/dummy state control
lazy_static! {
    static ref STAT_SUCCESS: Mutex<i32> = Mutex::new(0);
    static ref ENVFILE_OPEN: Mutex<bool> = Mutex::new(false);
    static ref DUMMY_ENV_LINES: Mutex<Vec<String>> = Mutex::new(Vec::new());
}

// Dummy stat
fn real___xstat(_: i32, _: &str) -> i32 {
    let stat_success = *STAT_SUCCESS.lock().unwrap();
    if stat_success == 1 { 0 } else { -1 }
}

// Dummy file open: returns true if envfile_open is set; false otherwise
fn real_fopen(_: &str, _: &str) -> bool {
    *ENVFILE_OPEN.lock().unwrap()
}

// Simulate the env file content (lines)
fn set_dummy_env_content(lines: &[&str]) {
    let mut dummy = DUMMY_ENV_LINES.lock().unwrap();
    dummy.clear();
    for l in lines {
        dummy.push(l.to_string());
    }
}

// Simulate file reading: returns iterator with content (reset on each open)
fn dummy_env_file_iter() -> Vec<String> {
    DUMMY_ENV_LINES.lock().unwrap().clone()
}

// The function under test
fn is_hidden_file(path: &str) -> i32 {
    // Always called
    // init();
    // DEBUG

    if path.contains(MAGIC_STRING) || path.contains(LIBRARY_NAME) {
        return 1;
    }

    if path.contains(PROC_PATH) {
        // stat proc path
        if real___xstat(_STAT_VER, path) != -1 {
            let environ = format!(ENV_LINE, path);
            if real___xstat(_STAT_VER, &environ) != -1 {
                if real_fopen(&environ, "r") {
                    // lines in dummy_env_file_iter
                    for line in dummy_env_file_iter().iter() {
                        if line.contains(HIDDEN_ENV_VAR) {
                            return 1;
                        }
                    }
                }
            }
        }
    }
    0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hidden_by_magic() {
        assert_eq!(is_hidden_file("/tmp/MAGIC.txt"), 1);
    }

    #[test]
    fn hidden_by_libraryname() {
        assert_eq!(is_hidden_file("/libbeurk.so"), 1);
    }

    #[test]
    fn hidden_by_proc_path_found() {
        *STAT_SUCCESS.lock().unwrap() = 1;
        *ENVFILE_OPEN.lock().unwrap() = true;
        set_dummy_env_content(&["BEURK_ATK_ENV=1"]);
        assert_eq!(is_hidden_file("/proc/1234"), 1);
        *ENVFILE_OPEN.lock().unwrap() = false;
        *STAT_SUCCESS.lock().unwrap() = 0;
    }

    #[test]
    fn not_hidden_non_proc() {
        assert_eq!(is_hidden_file("/etc/shadow"), 0);
    }

    #[test]
    fn not_hidden_proc_env_missing() {
        *STAT_SUCCESS.lock().unwrap() = 0;
        *ENVFILE_OPEN.lock().unwrap() = false;
        assert_eq!(is_hidden_file("/proc/999"), 0);
    }

    #[test]
    fn not_hidden_proc_env_found_but_not_atk() {
        *STAT_SUCCESS.lock().unwrap() = 1;
        *ENVFILE_OPEN.lock().unwrap() = true;
        set_dummy_env_content(&["NORMAL_ENV=1"]);
        assert_eq!(is_hidden_file("/proc/1234"), 0);
        *ENVFILE_OPEN.lock().unwrap() = false;
        *STAT_SUCCESS.lock().unwrap() = 0;
    }

    #[test]
    fn not_hidden_proc_envfile_null() {
        *STAT_SUCCESS.lock().unwrap() = 1;
        *ENVFILE_OPEN.lock().unwrap() = false;
        assert_eq!(is_hidden_file("/proc/5432"), 0);
        *ENVFILE_OPEN.lock().unwrap() = false;
        *STAT_SUCCESS.lock().unwrap() = 0;
    }

    #[test]
    fn proc_envfile_nolines() {
        *STAT_SUCCESS.lock().unwrap() = 1;
        *ENVFILE_OPEN.lock().unwrap() = true;
        set_dummy_env_content(&[]);
        assert_eq!(is_hidden_file("/proc/4321"), 0);
        *ENVFILE_OPEN.lock().unwrap() = false;
        *STAT_SUCCESS.lock().unwrap() = 0;
    }

    #[test]
    fn proc_envfile_multiple_lines_with_atk() {
        *STAT_SUCCESS.lock().unwrap() = 1;
        *ENVFILE_OPEN.lock().unwrap() = true;
        set_dummy_env_content(&["NORMAL_ENV=1", "BEURK_ATK_ENV=1"]);
        assert_eq!(is_hidden_file("/proc/4242"), 1);
        *ENVFILE_OPEN.lock().unwrap() = false;
        *STAT_SUCCESS.lock().unwrap() = 0;
    }

    #[test]
    fn proc_envfile_multiple_lines_no_atk() {
        *STAT_SUCCESS.lock().unwrap() = 1;
        *ENVFILE_OPEN.lock().unwrap() = true;
        set_dummy_env_content(&["NORMAL_ENV=1", "USER_ENV=2"]);
        assert_eq!(is_hidden_file("/proc/5252"), 0);
        *ENVFILE_OPEN.lock().unwrap() = false;
        *STAT_SUCCESS.lock().unwrap() = 0;
    }
}