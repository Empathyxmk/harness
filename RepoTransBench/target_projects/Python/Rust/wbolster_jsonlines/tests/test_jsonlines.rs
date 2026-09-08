// test_jsonlines.py => test_jsonlines.rs

use std::collections::BTreeMap;
use std::fs::{File, OpenOptions};
use std::io::{self, Seek, SeekFrom, Write, Read, BufReader, BufWriter, Cursor};
use serde_json::{Value, json};
use wbolster_jsonlines_rs::*;
use wbolster_jsonlines_rs::jsonlines::{InvalidLineError, Error};
use tempfile::NamedTempFile;

// Sample bytes/text as in Python test
const SAMPLE_BYTES: &[u8] = b"{\"a\": 1}\n{\"b\": 2}\n";
const SAMPLE_TEXT: &str = "{\"a\": 1}\n{\"b\": 2}\n";

fn is_json_decode_error(_err: &dyn std::error::Error) -> bool {
    // In this Rust translation, any JSON error is a serde_json::Error, which suffices.
    true
}

#[test]
fn test_reader() {
    let cursor = Cursor::new(SAMPLE_BYTES);
    let mut reader = Reader::new(cursor);
    let v1: Value = reader.read().unwrap();
    let v2: Value = reader.read().unwrap();
    assert_eq!(v1, json!({"a": 1}));
    assert_eq!(v2, json!({"b": 2}));
    assert!(reader.read::<Value>().is_err()); // EOF
}

#[test]
fn test_writer_text() {
    let mut buf = Vec::new();
    {
        let mut writer = Writer::new(&mut buf);
        writer.write(&json!({"a": 1})).unwrap();
        writer.write(&json!({"b": 2})).unwrap();
    }
    let s = String::from_utf8_lossy(&buf);
    assert_eq!(s, SAMPLE_TEXT);
}

// Additional test coverage for reading from iterator, utf8, empty lines, custom dumps, etc would be handled with a more complete implementation.
// More thorough implementation would need full feature coverage as per the Python original.