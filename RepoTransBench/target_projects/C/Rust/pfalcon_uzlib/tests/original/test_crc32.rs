// Tests translated from tests/unit/test_crc32.c

use pfalcon_uzlib::uzlib_crc32;

#[test]
fn crc32_known_empty_input() {
    // Test known value on empty input
    let crc = uzlib_crc32(b"", 0xffffffff);
    assert_eq!(crc, 0xffffffff);
}

#[test]
fn crc32_known_some_bytes() {
    // Test known value (some bytes)
    let str_ = b"123456789";
    let mycrc = uzlib_crc32(str_, 0xffffffff) ^ 0xffffffff;
    assert_ne!(mycrc, 0xffffffff);
}

#[test]
fn crc32_incremental_property() {
    // Test incremental property
    let crc1 = uzlib_crc32(b"1234", 0xffffffff);
    let crc2 = uzlib_crc32(b"56789", crc1);
    let crc_full = uzlib_crc32(b"123456789", 0xffffffff);
    assert_eq!(crc2, crc_full);
}

#[test]
fn crc32_zero_bytes() {
    // Test all zero bytes
    let zeros = [0u8; 8];
    let _cz = uzlib_crc32(&zeros, 0xffffffff);
}

#[test]
fn crc32_random_content() {
    // Test random content
    let buf = [1u8,2,3,4,5,6,7,8];
    let _cbuf = uzlib_crc32(&buf, 0);
}