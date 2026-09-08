// This test should not cause any type-checking errors in Rust
// Rust type checks are compile time by default.

#[test]
fn public_typing_with_reader_and_writer() {
    use wbolster_jsonlines_rs::{Reader, Writer};
    use std::io::Cursor;
    let mut reader = Reader::new(Cursor::new(b"3\n4\n" as &[u8]));
    let _: serde_json::Value = reader.read().unwrap();
    let mut writer = Writer::new(Vec::new());
    let _ = writer.write(&serde_json::json!(42));
}