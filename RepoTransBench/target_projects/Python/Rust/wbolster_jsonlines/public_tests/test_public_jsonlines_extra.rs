// Translated from test_public_jsonlines_extra.py (public version)

use wbolster_jsonlines_rs::*;
use wbolster_jsonlines_rs::jsonlines::{InvalidLineError, Error, ReaderWriterBase};
use std::fs::File;
use tempfile::tempdir;

#[test]
fn test_public_default_dumps_not_implemented() {
    let v = 123;
    let res = wbolster_jsonlines_rs::default_dumps(&v);
    assert!(res.is_err());
}

#[test]
fn test_public_invalid_line_error_properties() {
    let err = InvalidLineError::new("Oops", "another bad json", 7);
    assert_eq!(err.line, "another bad json");
    assert_eq!(err.lineno, 7);
    assert!(err.to_string().contains("Oops"));
    let err2 = InvalidLineError::new("Msg", "lineagain\n", 4);
    assert_eq!(err2.line, "lineagain");
}

#[test]
fn test_public_readerwriterbase_close_multiple() {
    let base = ReaderWriterBase::new();
    base.close();
    base.close();
}

#[test]
fn test_public_readerwriterbase_eq() {
    let base1 = ReaderWriterBase::new();
    let base2 = ReaderWriterBase::new();
    assert_eq!(base1, base2);
}

#[test]
fn test_public_writer_write_obj_types() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("public_test.jsonl");
    {
        let mut writer = Writer::new(File::create(&path).unwrap());
        writer.write(&serde_json::json!({"xyz": 15})).unwrap();
    }
    let f = File::open(&path).unwrap();
    let mut reader = Reader::new(f);
    let val: serde_json::Value = reader.read().unwrap();
    assert_eq!(val, serde_json::json!({"xyz": 15}));
}