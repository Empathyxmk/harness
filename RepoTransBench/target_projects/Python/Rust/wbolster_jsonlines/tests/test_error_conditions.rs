// test_error_conditions.py => test_error_conditions.rs

use wbolster_jsonlines_rs::*;
use wbolster_jsonlines_rs::jsonlines::ReaderWriterBase;

#[test]
fn test_readerwriterbase_repr() {
    let dummy = ReaderWriterBase::new();
    let result = dummy.to_string();
    assert!(result.contains("ReaderWriterBase"));
}

#[test]
fn test_readerwriterbase_close_closes_fp() {
    let dummy = ReaderWriterBase::new();
    dummy.close();
    assert!(dummy.is_closed());
}

#[test]
fn test_default_dumps_notimplemented() {
    let v = "abc";
    let res = wbolster_jsonlines_rs::default_dumps(&v);
    assert!(res.is_err());
}