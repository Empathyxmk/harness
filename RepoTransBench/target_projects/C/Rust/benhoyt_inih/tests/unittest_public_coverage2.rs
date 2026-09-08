//! Rust translation of tests/unittest_public_coverage2.c
use benhoyt_inih_rust::*;

fn handler_section_key_val_public(count: &mut i32, _section: &str, name: Option<&str>, _value: Option<&str>, _lineno: Option<usize>) -> i32 {
    if let Some("specialerror") = name {
        return -2;
    }
    *count += 1;
    3
}

fn test_public_bad_file() {
    let result = ini_parse("notfound_public.ini", &mut |_, _, _, _| 1, &mut ());
    println!("test_public_bad_file: {}", result);
}
fn test_public_bad_section() {
    let mut called = 0;
    let result = ini_parse("bad_multi.ini", &mut |section, name, value, _| handler_section_key_val_public(&mut called, section, Some(name), value, None), &mut called);
    println!("test_public_bad_section: {}, called={}", result, called);
}
fn test_public_bad_comment() {
    let mut called = 0;
    let result = ini_parse("bad_comment.ini", &mut |section, name, value, _| handler_section_key_val_public(&mut called, section, Some(name), value, None), &mut called);
    println!("test_public_bad_comment: {}, called={}", result, called);
}
fn test_public_long_section() {
    let mut called = 0;
    let result = ini_parse("long_section.ini", &mut |section, name, value, _| handler_section_key_val_public(&mut called, section, Some(name), value, None), &mut called);
    println!("test_public_long_section: {}, called={}", result, called);
}
fn test_public_bom() {
    let mut called = 0;
    let result = ini_parse("bom.ini", &mut |section, name, value, _| handler_section_key_val_public(&mut called, section, Some(name), value, None), &mut called);
    println!("test_public_bom: {}, called={}", result, called);
}

#[test]
fn public_coverage2() {
    test_public_bad_file();
    test_public_bad_section();
    test_public_bad_comment();
    test_public_long_section();
    test_public_bom();
}