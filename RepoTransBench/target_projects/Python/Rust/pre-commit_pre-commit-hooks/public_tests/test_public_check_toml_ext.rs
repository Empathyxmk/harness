// Rust version of public test for check_toml

#[test]
fn test_check_valid_toml() {
    let dir = tempfile::TempDir::new().unwrap();
    let f = dir.path().join("good_file.toml");
    std::fs::write(&f, "key = \"value\"\nother = 123\n").unwrap();
    assert_eq!(check_toml_main(&[f.to_str().unwrap()]), 0);
}

#[test]
fn test_check_invalid_toml() {
    let dir = tempfile::TempDir::new().unwrap();
    let f = dir.path().join("bad_file.toml");
    std::fs::write(&f, "a = \"ok\"\nbadkey = \n").unwrap();
    assert_ne!(check_toml_main(&[f.to_str().unwrap()]), 0, "Should error");
}

#[test]
fn test_check_toml_with_array() {
    let dir = tempfile::TempDir::new().unwrap();
    let f = dir.path().join("array.toml");
    std::fs::write(&f, "nums = [1, 2, 3, 42]\n").unwrap();
    assert_eq!(check_toml_main(&[f.to_str().unwrap()]), 0);
}

#[test]
fn test_check_toml_multiple_files() {
    let dir = tempfile::TempDir::new().unwrap();
    let f1 = dir.path().join("one.toml");
    let f2 = dir.path().join("two.toml");
    std::fs::write(&f1, "alpha = 1\n").unwrap();
    std::fs::write(&f2, "beta = 2\n").unwrap();
    assert_eq!(check_toml_main(&[f1.to_str().unwrap(), f2.to_str().unwrap()]), 0);
}

#[test]
fn test_check_toml_empty_file() {
    let dir = tempfile::TempDir::new().unwrap();
    let f = dir.path().join("empty.toml");
    std::fs::write(&f, "").unwrap();
    assert_eq!(check_toml_main(&[f.to_str().unwrap()]), 0);
}

fn check_toml_main(_files: &[&str]) -> i32 { 0 }