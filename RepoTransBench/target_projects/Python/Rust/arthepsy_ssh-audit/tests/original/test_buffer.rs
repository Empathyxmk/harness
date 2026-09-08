// Rust translation of test/test_buffer.py
// Adapted to Rust test idioms, using `#[test]` and assert macros, and matching buffer w/byte helper logic.

use regex::Regex;
use lazy_static::lazy_static;

// Helper utility to parse hex into bytes
fn b(v: &str) -> Vec<u8> {
    let re = Regex::new(r"\s").unwrap();
    let cleaned = re.replace_all(v, "");
    let bytes: Vec<u8> = cleaned
        .as_bytes()
        .chunks(2)
        .map(|s| u8::from_str_radix(std::str::from_utf8(s).unwrap(), 16).unwrap())
        .collect();
    bytes
}

#[test]
fn test_unread() {
    // TODO: convert this test fully with accurate WriteBuf/ReadBuf usage.
    // assert logic goes here.
}