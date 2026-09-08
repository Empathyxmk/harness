// Minimal stub translated from public_tests/test_public_error_conditions.py

use wbolster_jsonlines_rs::*;
use serde_json::json;
use tempfile::tempdir;
use std::fs::{File, OpenOptions};
use std::io::{Read, Write, Seek, SeekFrom};

#[test]
fn test_public_writer_non_dict() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("pub_test2.jsonl");

    {
        let mut f = File::create(&path).unwrap();
        let mut writer = Writer::new(&mut f);
        writer.write(&"something completely else").unwrap();
        writer.write(&3.1415).unwrap();
    }
    let mut f = File::open(&path).unwrap();
    let mut s = String::new();
    f.read_to_string(&mut s).unwrap();
    let lines: Vec<&str> = s.split('\n').collect();
    assert!(lines[0].contains("something completely else"));
    assert!(lines[1].contains("3.1415"));
}