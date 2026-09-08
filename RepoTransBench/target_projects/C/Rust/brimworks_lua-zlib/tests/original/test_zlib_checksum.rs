// Translated from test_zlib_checksum.lua

use lua_zlib::*;

#[test]
fn test_adler32_hello() {
    let data = "hello";
    let ad = adler32(data);
    assert_eq!(ad, 92507769, "adler32 correct value");
}

#[test]
fn test_crc32_hello() {
    let data = "hello";
    let crc = crc32(data);
    assert_eq!(crc, 907060870, "crc32 correct value");
}

#[test]
fn test_adler32_empty() {
    let ad_empty = adler32("");
    assert_eq!(ad_empty, 1, "adler32 empty string is 1");
}

#[test]
fn test_crc32_empty() {
    let crc_empty = crc32("");
    assert_eq!(crc_empty, 0, "crc32 empty string is 0");
}