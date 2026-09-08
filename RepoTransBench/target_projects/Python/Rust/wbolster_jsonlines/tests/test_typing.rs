// test_typing.py => test_typing.rs
// This test checks that the Rust type system provides compile-time checks for types.
// Rust typing is stricter; here we just compile to ensure (no run-time assertions).

#[allow(dead_code)]
fn something_with_reader() {
    use wbolster_jsonlines_rs::Reader;
    // &str, &[u8], Vec<String> -- Reader can be generic in real use.
    let mut reader = Reader::new(std::io::Cursor::new(b"[1]\n[2]\n" as &[u8]));
    let _r1: serde_json::Value = reader.read().unwrap_or_default();
}

#[allow(dead_code)]
fn something_with_writer() {
    use wbolster_jsonlines_rs::Writer;
    let mut writer = Writer::new(Vec::new());
    let _ = writer.write(&serde_json::json!([1, 2, 3]));
}

// Real type checks in Rust occur at compile time not via tests, so "type check" tests are effectively no-ops here.