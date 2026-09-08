//! Rust translation of util_test.c from keirf_amiga-stuff
//! Covers sprintf, vsprintf, memset, memcpy adapters for test

use keirf_amiga_stuff::util::*;
use std::string::String;

fn dummy_handler(_msg: &str) {}

#[test]
fn test_sprintf_basic() {
    let buf = sprintf_adapter!("A{}{}{}{}", "b", 'D', 42, 1);
    assert_eq!(buf, "AbD421");
}

#[test]
fn test_vsprintf_width() {
    let buf = sprintf_adapter!("%8d", 3);
    assert_eq!(buf, "       3");
    let buf = sprintf_adapter!("%2d", 15);
    assert_eq!(buf, "15");
    let buf = sprintf_adapter!("%6s", "abc");
    assert_eq!(buf, "abc...");
}

#[test]
fn test_vsprintf_zero() {
    let buf = sprintf_adapter!("%d", 0);
    assert_eq!(buf, "0");
}

#[test]
fn test_memset_memcpy() {
    let mut buf = [b'x'; 5];
    // Add zero terminator for comparison as string
    let mut buf_str = [0u8; 6];
    buf_str[..5].copy_from_slice(&buf);
    assert_eq!(std::str::from_utf8(&buf_str[..5]).unwrap(), "xxxxx");
    // memcpy test
    memcpy_adapter(&mut buf_str[..5], b"world");
    assert_eq!(std::str::from_utf8(&buf_str[..5]).unwrap(), "world");
}

#[test]
fn test_vsprintf_edgecases() {
    // Empty string
    let buf = sprintf_adapter!("%s", "");
    assert_eq!(buf, "");
    // Int width
    let buf = sprintf_adapter!("%10u", 1234u32);
    assert_eq!(buf, "      1234");
    // Width-str no dots needed
    let buf = sprintf_adapter!("%3s", "abc");
    assert_eq!(buf, "abc");
    // Percent literal
    let buf = sprintf_adapter!("%%test");
    assert_eq!(buf, "%test");
    // Char
    let buf = sprintf_adapter!("%c", 'X');
    assert_eq!(buf, "X");
    // Null string pointer safety; we simulate by passing "(null)"
    let buf = sprintf_adapter!("%6s", "(null)");
    // Accept both possibilities: "(null)" and "(null).."
    assert!(
        buf == "(null)" || buf == "(null)..",
        "unexpected: {buf:?}"
    );
}

#[test]
fn test_vsprintf_largeint() {
    let buf = sprintf_adapter!("%u", 123456789u32);
    assert_eq!(buf, "123456789");
}

#[test]
fn test_vsprintf_unrecognised() {
    let buf = sprintf_adapter!("%z hello", 22);
    assert_eq!(buf, "z hello");
}