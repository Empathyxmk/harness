// Public tests for librope - translation of test/tests_public.c

use librope::{Rope, RopeResult::*};

fn check(r: &Rope, expected: &str) {
    assert_eq!(r.byte_count(), expected.len());
    let cstr = r.create_cstr();
    let s = std::str::from_utf8(&cstr[..cstr.len().saturating_sub(1)]).unwrap_or("");
    assert_eq!(s, expected);
}

fn checked_insert(r: &mut Rope, pos: usize, s: &str) {
    assert_eq!(r.insert(pos, s.as_bytes()), Ok);
}

#[test]
fn test_empty_rope_has_no_content_public() {
    let r = Rope::new();
    check(&r, "");
    assert_eq!(r.char_count(), 0);
    let bytes = r.create_cstr();
    assert_eq!(bytes[0], 0);
    r.free();
}

#[test]
fn test_insert_at_location_public() {
    let mut r = Rope::new();
    checked_insert(&mut r, 0, "XYZ");
    check(&r, "XYZ");
    checked_insert(&mut r, 0, "MMN");
    check(&r, "MMNXYZ");
    checked_insert(&mut r, 6, "OPQ");
    check(&r, "MMNXYZOPQ");
    checked_insert(&mut r, 3, "999");
    check(&r, "MMN999XYZOPQ");
    assert_eq!(r.char_count(), 12);
    r.free();
}

fn check_invalid_public(err_str: &[u8]) {
    let mut r = Rope::new();
    let res = r.insert(0, err_str);
    assert_eq!(res, InvalidUtf8);
    assert_eq!(r.char_count(), 0);
    assert_eq!(r.byte_count(), 0);
    r.free();
}

#[test]
fn test_invalid_utf8_rejected_public() {
    check_invalid_public(&[0xf0, 0]);
    check_invalid_public(&[0xa0, 0]);
    check_invalid_public(&[0xe0, 0xa0, 0]);
    check_invalid_public(&[0xd0, 0xd0, 0xa0, 0]);
}

#[test]
fn test_new_string_has_content_public() {
    let r = Rope::new_with_utf8("Hello world".as_bytes()).unwrap();
    check(&r, "Hello world");
    assert_eq!(r.char_count(), "Hello world".len());
    r.free();

    let mut r = Rope::new_with_utf8("аврора".as_bytes()).unwrap();
    check(&r, "аврора");
    assert_eq!(r.char_count(), 6);
    r.insert(4, "🔥🌞".as_bytes());
    check(&r, "авро🔥🌞ра");
    assert_eq!(r.char_count(), 8);
    r.free();
}

#[test]
fn test_delete_at_location_public() {
    let mut r = Rope::new_with_utf8("ABCDEFGHIJ".as_bytes()).unwrap();
    r.del(1, 1);
    check(&r, "ACDEFGHIJ");
    r.del(3, 2);
    check(&r, "ACDGHIJ");
    r.del(2, 3);
    check(&r, "ACIJ");
    r.del(0, 2);
    check(&r, "IJ");
    r.del(0, 10);
    check(&r, "");
    assert_eq!(r.char_count(), 0);
    r.free();
}

#[test]
fn test_delete_past_end_of_string_public() {
    let mut r = Rope::new();
    r.del(0, 42);
    check(&r, "");
    r.insert(0, b"public test");
    r.del(7, 50);
    check(&r, "public ");
    assert_eq!(r.char_count(), 7);
    r.free();
}