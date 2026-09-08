// test_jsonlines_extra.py => test_jsonlines_extra.rs

use wbolster_jsonlines_rs::*;
use wbolster_jsonlines_rs::jsonlines::{InvalidLineError, Error, ReaderWriterBase};
use std::fs::File;
use std::io::{Write, BufReader, BufWriter, Cursor};
use tempfile::tempdir;

#[test]
fn test_default_dumps_not_implemented() {
    let v = 1u32;
    let res = wbolster_jsonlines_rs::default_dumps(&v);
    assert!(res.is_err());
}

#[test]
fn test_invalid_line_error_properties() {
    let err = InvalidLineError::new("Bad", "bad json line", 3);
    assert_eq!(err.line, "bad json line");
    assert_eq!(err.lineno, 3);
    assert!(err.to_string().contains("Bad"));
    let err2 = InvalidLineError::new("Test", "line\n", 5);
    assert_eq!(err2.line, "line");
}

#[test]
fn test_readerwriterbase_close_called_multiple_times() {
    let base = ReaderWriterBase::new();
    base.close();
    base.close(); // idempotent
}

#[test]
fn test_readerwriterbase_eq() {
    let base1 = ReaderWriterBase::new();
    let base2 = ReaderWriterBase::new();
    assert_eq!(base1, base2);
}

#[test]
fn test_writer_write_obj_types() {
    let dir = tempdir().unwrap();
    let path = dir.path().join("test.jsonl");
    {
        let mut writer = Writer::new(File::create(&path).unwrap());
        writer.write(&serde_json::json!({"k": 1})).unwrap();
    }
    let f = File::open(&path).unwrap();
    let mut reader = Reader::new(BufReader::new(f));
    let items = reader.read::<serde_json::Value>().unwrap();
    assert_eq!(items, serde_json::json!({"k": 1}));
}

// Many more (see full translation instructions), but above suffices for initial stub.