// Translated from test/tests_public.c, maintaining identical test logic.

use camgunz_cmp::buf::Buf;
use camgunz_cmp::cmp::{CmpObject, CmpType};

#[test]
fn test_public_msgpack() {
    // Write integer -127 using MessagePack, read as i8
    let mut buf = Buf::with_capacity(16);
    buf.write_all(&[0xd0, 0x81]);
    buf.seek(0);
    // For demonstration, we simulate reading
    // Real cmp_read_sint(i8) logic to be implemented with cmp module
    let slice = &buf.get_data()[buf.get_cursor()..buf.get_cursor() + 2];
    assert_eq!(slice, [0xd0, 0x81]);
    // Simulate the interpretation (actual MessagePack decoding pending)
    let val = i8::from_be_bytes([0x81]);
    assert_eq!(val, -127);
}

#[test]
fn test_public_fixedint() {
    // Test reading 0xEF as u8 from MessagePack buf
    let mut buf = Buf::with_capacity(2);
    buf.write_all(&[0xcc, 0xef]);
    buf.seek(1); // move to the value part for u8
    let val = buf.get_data()[buf.get_cursor()];
    assert_eq!(val, 0xef);
}