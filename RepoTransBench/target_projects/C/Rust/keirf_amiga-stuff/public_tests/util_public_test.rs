//! Rust public test for util_public_test.c from keirf_amiga-stuff

use keirf_amiga_stuff::util::*;
use std::string::String;

#[test]
fn test_sprintf_basic_public() {
    let buf = sprintf_adapter!("%c{}{}{}", 'Z', "oo", 123, 0);
    assert_eq!(buf, "Zoo1230");
    let buf = sprintf_adapter!("HELLO");
    assert_eq!(buf, "HELLO");
}

#[test]
fn test_vsprintf_width_public() {
    let buf = sprintf_adapter!("%4d", 17);
    assert_eq!(buf, "  17");
    let buf = sprintf_adapter!("%7d", 31);
    assert_eq!(buf, "     31");
    let buf = sprintf_adapter!("%5s", "xyz");
    assert_eq!(buf, "xyz..");
}

#[test]
fn test_vsprintf_zero_public() {
    let buf = sprintf_adapter!("%d", 0u32);
    assert_eq!(buf, "0");
}

#[test]
fn test_memset_memcpy_public() {
    let mut buf = [b'*'; 4];
    let mut buf_str = [0u8; 5];
    buf_str[..4].copy_from_slice(&buf);
    assert_eq!(std::str::from_utf8(&buf_str[..4]).unwrap(), "****");
    memcpy_adapter(&mut buf_str[..4], b"data");
    assert_eq!(std::str::from_utf8(&buf_str[..4]).unwrap(), "data");
}

#[test]
fn test_vsprintf_edgecases_public() {
    let buf = sprintf_adapter!("%s", "PUBLIC");
    assert_eq!(buf, "PUBLIC");
    let buf = sprintf_adapter!("%8u", 4321u32);
    assert_eq!(buf, "    4321");
    let buf = sprintf_adapter!("%4s", "x");
    assert_eq!(buf, "x...");
    let buf = sprintf_adapter!("%%%%");
    assert_eq!(buf, "%%");
    let buf = sprintf_adapter!("%c", 'P');
    assert_eq!(buf, "P");
    let buf = sprintf_adapter!("%7s", "(null)");
    assert!(
        buf == "(null).." || buf == "(null)",
        "unexpected: {buf:?}"
    );
}