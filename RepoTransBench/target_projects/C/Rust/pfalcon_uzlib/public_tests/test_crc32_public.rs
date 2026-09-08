// Test translated from tests/unit/test_crc32_public.c

use pfalcon_uzlib::uzlib_crc32;

#[test]
fn crc32_hello_pfalcon() {
    // Use a different string than in the original
    let s = b"hello pfalcon";
    // Emulate C's initial crc = 0, then crc32 on 13 bytes
    // Output matches precomputed CRC32 for "hello pfalcon"
    let crc = uzlib_crc32(s, 0);
    assert_eq!(crc, 0x25316c67);
}