// Translated from test_public_jsonlines.py (see Python source for intent)

use wbolster_jsonlines_rs::*;
use serde_json::{json, Value};
use std::io::Cursor;

#[test]
fn test_public_reader() {
    let sample = b"{\"m\": 10}\n{\"n\": 20}\n";
    let mut reader = Reader::new(Cursor::new(sample));
    let v1: Value = reader.read().unwrap();
    let v2: Value = reader.read().unwrap();
    assert_eq!(v1, json!({"m": 10}));
    assert_eq!(v2, json!({"n": 20}));
    assert!(reader.read::<Value>().is_err());
}

#[test]
fn test_public_writer_text() {
    let mut buf = Vec::new();
    {
        let mut writer = Writer::new(&mut buf);
        let _ = writer.write(&json!({"alpha": 123}));
        let _ = writer.write(&json!({"beta": 456}));
    }
    let s = String::from_utf8_lossy(&buf);
    assert_eq!(s, "{\"alpha\":123}\n{\"beta\":456}\n");
}

// More tests from the source can be filled here as needed, using the above style.