use std::fs::{self, File};
use std::io::{Write, Read};
use std::path::Path;
use tempfile::tempdir;
use regex::Regex;

/// Simulates the `read` function from Python setup.py and checks file reading.
#[test]
fn test_read_reads_file() {
    let dir = tempdir().unwrap();
    let pkg_dir = dir.path().join("flask_redis");
    fs::create_dir(&pkg_dir).unwrap();
    let file_path = pkg_dir.join("dummy.py");
    let test_text = "abc";
    fs::write(&file_path, test_text).unwrap();

    // Simulate a setup.py's read function
    let read = |paths: &[&str]| -> String {
        let here = dir.path();
        let mut full = here.to_path_buf();
        for p in paths {
            full.push(p);
        }
        fs::read_to_string(full).unwrap()
    };

    let result = read(&["flask_redis", "dummy.py"]);
    assert_eq!(result, test_text);
}

#[test]
fn test_find_meta_success() {
    // Simulate finding meta (__title__, __description__) using regex
    fn read() -> String {
        "__title__ = 'foo'\n__description__ = 'bar'".to_string()
    }

    fn find_meta(meta: &str) -> String {
        let re_txt = format!(r#"__{}__\s*=\s*['"]([^'"]*)['"]"#, regex::escape(meta));
        let re = Regex::new(&re_txt).unwrap();
        let content = read();
        let cap = re.captures(&content).expect("Meta not found");
        cap.get(1).unwrap().as_str().to_string()
    }

    assert_eq!(find_meta("title"), "foo");
    assert_eq!(find_meta("description"), "bar");
}

#[test]
#[should_panic(expected = "Meta not found")]
fn test_find_meta_failure() {
    fn read() -> String { "".to_string() }
    fn find_meta(meta: &str) -> String {
        let re_txt = format!(r#"__{}__\s*=\s*['"]([^'"]*)['"]"#, regex::escape(meta));
        let re = Regex::new(&re_txt).unwrap();
        let content = read();
        let cap = re.captures(&content).expect("Meta not found");
        cap.get(1).unwrap().as_str().to_string()
    }
    find_meta("whatever");
}