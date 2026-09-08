use std::fs;
use std::io::Write;
use tempfile::tempdir;
use regex::Regex;

#[test]
fn test_read_reads_file_public() {
    let dir = tempdir().unwrap();
    let pkg_dir = dir.path().join("flask_redis");
    fs::create_dir(&pkg_dir).unwrap();
    let file_path = pkg_dir.join("testfile_public.txt");
    let test_text = "123xyz";
    fs::write(&file_path, test_text).unwrap();

    let read = |paths: &[&str]| -> String {
        let here = dir.path();
        let mut full = here.to_path_buf();
        for p in paths {
            full.push(p);
        }
        fs::read_to_string(full).unwrap()
    };

    let result = read(&["flask_redis", "testfile_public.txt"]);
    assert_eq!(result, test_text);
}

#[test]
fn test_find_meta_success_public() {
    fn read() -> String {
        "__spam__ = 'eggs'\n__hamp__ = 'bacon'".to_string()
    }
    fn find_meta(meta: &str) -> String {
        let re_txt = format!(r#"__{}__\s*=\s*['"]([^'"]*)['"]"#, regex::escape(meta));
        let re = Regex::new(&re_txt).unwrap();
        let content = read();
        let cap = re.captures(&content).expect("Meta not found");
        cap.get(1).unwrap().as_str().to_string()
    }
    assert_eq!(find_meta("spam"), "eggs");
    assert_eq!(find_meta("hamp"), "bacon");
}

#[test]
#[should_panic(expected = "Meta not found")]
fn test_find_meta_failure_public() {
    fn read() -> String { "".to_string() }
    fn find_meta(meta: &str) -> String {
        let re_txt = format!(r#"__{}__\s*=\s*['"]([^'"]*)['"]"#, regex::escape(meta));
        let re = Regex::new(&re_txt).unwrap();
        let content = read();
        let cap = re.captures(&content).expect("Meta not found");
        cap.get(1).unwrap().as_str().to_string()
    }
    find_meta("somethingelse");
}