// Translated from test_zlib_checksum_public.lua

use lua_zlib::*;

#[test]
fn test_adler32_public_value() {
    let data = "world";
    let ad = adler32(data);
    assert_eq!(ad, 113330241, "adler32 public value correct");
}

#[test]
fn test_crc32_public_value() {
    let data = "publictest";
    let crc = crc32(data);
    assert_eq!(crc, 4132549654, "crc32 public value correct");
}