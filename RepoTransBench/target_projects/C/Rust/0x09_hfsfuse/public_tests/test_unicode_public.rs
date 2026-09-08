use crate::unicode::*;
use std::ffi::CString;

#[test]
fn test_utf8_to_utf16_ascii_public() {
    // "Hello, Test!"
    let src = "Hello, Test!";
    let mut dst = [0u16; 256];
    let outlen = utf8_to_utf16(&mut dst, src, false, &mut 0);
    assert_eq!(outlen, src.len());
    for (i, &ch) in src.as_bytes().iter().enumerate() {
        assert_eq!(dst[i], ch as u16);
    }
}

#[test]
fn test_utf8_to_utf16_emoji_public() {
    // "Good \xF0\x9F\x98\x8A luck."
    let src = "Good \u{1F60A} luck.";
    let mut dst = [0u16; 256];
    let outlen = utf8_to_utf16(&mut dst, src, false, &mut 0);
    // 5 "Good ", emoji (2 surrogates), " luck." (6) = 13 u16 units
    assert_eq!(outlen, 13);
    assert_eq!(dst[5], 0xD83D); // high surrogate
    assert_eq!(dst[6], 0xDE0A); // low surrogate
}

#[test]
fn test_utf8_to_utf16_invalid2byte_public() {
    // 0xC2 as stand-alone, missing continuation
    let src_bytes = b"ABC\xC2Z";
    let src = std::str::from_utf8(src_bytes).unwrap_or("\u{FFFD}");
    let mut dst = [0u16; 256];
    let mut err = 0;
    let outlen = utf8_to_utf16(&mut dst, src, true, &mut err);
    // Should substitute the invalid byte, so length == 5, error nonzero
    assert_eq!(outlen, src.chars().count());
    assert_ne!(err, 0);
}

#[test]
fn test_utf16_to_utf8_cyrillic_public() {
    // "Привет!" in Cyrillic
    let src = [0x041F, 0x0440, 0x0438, 0x0432, 0x0435, 0x0442, 0x21, 0x0];
    let mut dst = [0u8; 64];
    let mut err = 0;
    let outlen = utf16_to_utf8(&mut dst, &src[..7], false, &mut err);
    let expect = "Привет!";
    assert_eq!(std::str::from_utf8(&dst[..outlen]).unwrap(), expect);
    assert_eq!(outlen, expect.len());
}

#[test]
fn test_utf16_to_utf8_surrogate_public() {
    // Music G Clef U+1D11E -> D834 DD1E
    let src = [0xD834, 0xDD1E, 0x0];
    let mut dst = [0u8; 16];
    let mut err = 0;
    let outlen = utf16_to_utf8(&mut dst, &src[..2], false, &mut err);
    // "\xF0\x9D\x84\x9E" is UTF-8 for U+1D11E
    assert_eq!(&dst[..outlen], b"\xF0\x9D\x84\x9E");
    assert_eq!(outlen, 4);
}

#[test]
fn test_utf8_to_utf16_unexpected_continuation_public() {
    let src_bytes = b"XY\x80Z";
    let src = std::str::from_utf8(src_bytes).unwrap_or("\u{FFFD}");
    let mut dst = [0u16; 16];
    let mut err = 0;
    let outlen = utf8_to_utf16(&mut dst, src, true, &mut err);
    assert_eq!(outlen, src.chars().count());
    assert_ne!(err, 0);
}