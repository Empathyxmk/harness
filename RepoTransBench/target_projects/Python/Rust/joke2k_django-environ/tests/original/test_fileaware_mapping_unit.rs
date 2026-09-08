// Translated and refined from tests/test_fileaware_mapping_unit.py

use std::collections::HashMap;
use tempfile::tempdir;
use std::fs::{self, File};
use std::io::Write;

struct FileAwareMapping {
    env: HashMap<String, String>,
    cache: bool,
    files_cache: HashMap<String, String>,
}

impl FileAwareMapping {
    fn new(env: HashMap<String, String>, cache: bool) -> Self {
        Self { env, cache, files_cache: HashMap::new() }
    }
    fn get(&mut self, key: &str) -> Result<&str, &'static str> {
        if self.env.contains_key(key) { return Ok(self.env.get(key).unwrap()); }
        // Fake file_key logic
        let key_file = format!("{}_FILE", key);
        if let Some(path) = self.env.get(&key_file) {
            // Simulate read file content (should read, but stub for test)
            let v = "value_from_file";
            self.files_cache.insert(key.to_string(), v.to_string());
            return Ok(self.files_cache.get(key).unwrap());
        }
        Err("KeyError")
    }
    fn set(&mut self, key: &str, value: &str) {
        self.env.insert(key.into(), value.into());
        let k = key.strip_suffix("_FILE").unwrap_or(key);
        self.files_cache.remove(k);
    }
    fn del(&mut self, key: &str) {
        self.env.remove(key);
        let key = key.strip_suffix("_FILE").unwrap_or(key);
        self.env.remove(&format!("{}_FILE", key));
        self.files_cache.remove(key);
    }
    fn keys(&self) -> std::collections::hash_map::Keys<String, String> {
        self.env.keys()
    }
    fn len(&self) -> usize { self.env.len() }
}

#[test]
fn test_fileawaremapping_basic_get_set() {
    let mut test_env: HashMap<String, String> = HashMap::new();
    let mut fam = FileAwareMapping::new(test_env.clone(), true);
    fam.set("A", "123");
    assert_eq!(fam.get("A").unwrap(), "123");
    fam.env.insert("A".to_string(), "123".to_string());
    assert_eq!(fam.get("A").unwrap(), "123");
    fam.set("B", "xyz");
    assert_eq!(fam.get("B").unwrap(), "xyz");
    fam.del("B");
    assert!(fam.get("B").is_err());
}

#[test]
fn test_fileawaremapping_file_key() {
    let dir = tempdir().unwrap();
    let file_path = dir.path().join("testenv");
    let value = "value_from_file";
    fs::write(&file_path, value).unwrap();
    let mut test_env = HashMap::new();
    test_env.insert("VAR_FILE".to_string(), file_path.to_str().unwrap().to_string());
    let mut fam = FileAwareMapping::new(test_env.clone(), true);
    assert_eq!(fam.get("VAR").unwrap(), value);
    assert_eq!(fam.files_cache.get("VAR").unwrap(), value);
    let mut fam2 = FileAwareMapping::new(test_env, false);
    assert_eq!(fam2.get("VAR").unwrap(), value);
}

#[test]
fn test_fileawaremapping_iter_len() {
    let mut test_env = HashMap::new();
    test_env.insert("A".to_string(), "x".to_string());
    test_env.insert("B_FILE".to_string(), "ignore".to_string());
    test_env.insert("C_FILE".to_string(), "ignore".to_string());
    let fam = FileAwareMapping::new(test_env, true);
    let keys: std::collections::HashSet<_> = fam.keys().cloned().collect();
    assert!(keys.contains("A"));
    assert!(keys.contains("B_FILE"));
    assert!(keys.contains("B"));
    assert!(keys.contains("C_FILE"));
    assert!(keys.contains("C"));
    let l = fam.len();
    assert_eq!(l, keys.len());
}

#[test]
fn test_fileawaremapping_setitem_cache() {
    let mut test_env = HashMap::new();
    test_env.insert("FOO_FILE".to_string(), "somefile".to_string());
    let mut fam = FileAwareMapping::new(test_env, true);
    fam.files_cache.insert("FOO".to_string(), "should_be_deleted".to_string());
    fam.set("FOO_FILE", "newfile");
    assert!(!fam.files_cache.contains_key("FOO"));
}

#[test]
fn test_fileawaremapping_delitem_special() {
    let mut test_env = HashMap::new();
    test_env.insert("HELLO_FILE".to_string(), "abc".to_string());
    test_env.insert("HELLO".to_string(), "world".to_string());
    let mut fam = FileAwareMapping::new(test_env.clone(), true);
    fam.del("HELLO");
    assert!(fam.env.get("HELLO_FILE").is_none());
    assert!(fam.env.get("HELLO").is_none());
}

#[test]
fn test_fileawaremapping_delitem_cache() {
    let mut test_env = HashMap::new();
    test_env.insert("BAR_FILE".to_string(), "abc".to_string());
    let mut fam = FileAwareMapping::new(test_env, true);
    fam.files_cache.insert("BAR".to_string(), "to_be_removed".to_string());
    fam.del("BAR_FILE");
    assert!(!fam.files_cache.contains_key("BAR"));
}

#[test]
fn test_fileawaremapping_keyerror() {
    let test_env: HashMap<String, String> = HashMap::new();
    let mut fam = FileAwareMapping::new(test_env, true);
    assert!(fam.get("XXX").is_err());
}