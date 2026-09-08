use crate::unicode::*;
use std::ffi::CString;
use std::os::raw::c_char;

/// Helper: convert &str <=> &[u8] as C would
fn as_bytes(s: &str) -> &[u8] { s.as_bytes() }

#[test]
fn test_ascii_to_utf16_roundtrip() {
    let ascii = "hello";
    let mut utf16 = [0u16; 10];
    let mut utf8 = [0u8; 10];
    let mut err = 0;

    let u16len = utf8_to_utf16(&mut utf16, ascii, false, &mut err);
    assert_eq!(err, 0);
    assert_eq!(u16len, ascii.len());

    let utf16_slice = &utf16[..u16len];
    let u8len = utf16_to_utf8(&mut utf8, utf16_slice, false, &mut err);
    assert_eq!(err, 0);
    assert_eq!(u8len, ascii.len());

    let utf8_str = std::str::from_utf8(&utf8[..u8len]).unwrap();
    assert_eq!(ascii, utf8_str);
}

#[test]
fn test_utf8_to_utf16_invalid() {
    // Invalid: UTF-8 >= 0xF5
    let invalid = vec![0xF5u8];
    let mut utf16 = [0u16; 2];
    let mut err = 0;
    // Simulate C-like interface.
    let s = std::str::from_utf8(&invalid).unwrap_or("\u{FFFD}");
    let outlen = utf8_to_utf16(&mut utf16, s, true, &mut err);
    assert!(outlen == s.chars().count() && err != 0);
}

#[test]
fn test_utf8_to_utf16_overlong() {
    // Overlong: 0xC0 0xAF
    let overlong = [0xC0u8, 0xAF];
    let mut utf16 = [0u16; 2];
    let mut err = 0;
    let s = std::str::from_utf8(&overlong).unwrap_or("\u{FFFD}");
    let outlen = utf8_to_utf16(&mut utf16, s, true, &mut err);
    assert!(outlen == s.chars().count() && err != 0);
}

#[test]
fn test_utf16_to_utf8_surrogate() {
    // Single surrogate, invalid
    let sur = [0xD800u16, 0u16];
    let mut utf8 = [0u8; 10];
    let mut err = 0;
    let outlen = utf16_to_utf8(&mut utf8, &sur[..1], true, &mut err);
    assert!(outlen == 0 && err != 0);
}

#[test]
fn test_utf8_nullptrs() {
    let mut err = -1;
    // Bad: dst=NULL, src=NULL
    let outlen = utf8_to_utf16(&mut [], "", false, &mut err);
    assert_eq!(outlen, 0);
    assert_ne!(err, 0);
}

#[test]
fn test_utf16_nullptrs() {
    let mut err = -1;
    let outlen = utf16_to_utf8(&mut [], &[], false, &mut err);
    assert_eq!(outlen, 0);
    assert_ne!(err, 0);
}

#[test]
fn test_utf8_zerolen() {
    let mut utf16 = [0u16; 1];
    let mut err = -1;
    let outlen = utf8_to_utf16(&mut utf16, "", false, &mut err);
    assert_eq!(outlen, 0);
    assert_eq!(err, 0);
}

#[test]
fn test_utf16_zerolen() {
    let mut out = [0u8; 1];
    let mut err = -1;
    let zeroed: [u16; 1] = [0u16];
    let outlen = utf16_to_utf8(&mut out, &zeroed[..0], false, &mut err);
    assert_eq!(outlen, 0);
    assert_eq!(err, 0);
}

#[test]
fn test_utf8_to_utf16_dstlen_zero() {
    let ascii = "a";
    let mut err = 0;
    let outlen = utf8_to_utf16(&mut [], ascii, false, &mut err);
    assert_eq!(outlen, 0);
    assert_eq!(err, 1);
}

#[test]
fn test_utf16_to_utf8_dstlen_zero() {
    let inbuf = [10u16, 0u16];
    let mut err = 0;
    let outlen = utf16_to_utf8(&mut [], &inbuf[..1], false, &mut err);
    assert_eq!(outlen, 0);
    assert_eq!(err, 1);
}

#[test]
fn test_utf8_to_utf16_short_dst() {
    let ascii = "abcdef";
    let mut utf16 = [0u16; 2];
    let mut err = 42;
    let out = utf8_to_utf16(&mut utf16, ascii, false, &mut err);
    assert_eq!(err, 0);
    assert_eq!(out, 2);
}

#[test]
fn test_utf16_to_utf8_short_dst() {
    let utf16 = ['a' as u16, 'b' as u16, 'c' as u16, 'd' as u16, 'e' as u16, 0u16];
    let mut out = [0u8; 2];
    let mut err = 42;
    let outlen = utf16_to_utf8(&mut out, &utf16[..5], false, &mut err);
    assert_eq!(err, 0);
    assert_eq!(outlen, 2);
}