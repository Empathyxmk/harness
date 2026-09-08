//! Rust translation of tests/unittest_coverage2.c
use benhoyt_inih_rust::*;

fn handler_section_key_val(count: &mut i32, _section: &str, name: Option<&str>, _value: Option<&str>, _lineno: Option<usize>) -> i32 {
    if let Some("errorkey") = name {
        return -1;
    }
    *count += 1;
    2
}

fn test_bad_file() {
    let result = ini_parse("doesnotexist.ini", &mut |_, _, _, _| 1, &mut ());
    println!("test_bad_file: {}", result);
}

fn test_bad_section() {
    let mut called = 0;
    let result = ini_parse("bad_section.ini", &mut |section, name, value, _| handler_section_key_val(&mut called, section, Some(name), value, None), &mut called);
    println!("test_bad_section: {}, called={}", result, called);
}

fn test_bad_comment() {
    let mut called = 0;
    let result = ini_parse("bad_comment.ini", &mut |section, name, value, _| handler_section_key_val(&mut called, section, Some(name), value, None), &mut called);
    println!("test_bad_comment: {}, called={}", result, called);
}

fn test_long_line() {
    let mut called = 0;
    let result = ini_parse("long_line.ini", &mut |section, name, value, _| handler_section_key_val(&mut called, section, Some(name), value, None), &mut called);
    println!("test_long_line: {}, called={}", result, called);
}

fn test_duplicate_sections() {
    let mut called = 0;
    let result = ini_parse("duplicate_sections.ini", &mut |section, name, value, _| handler_section_key_val(&mut called, section, Some(name), value, None), &mut called);
    println!("test_duplicate_sections: {}, called={}", result, called);
}

#[test]
fn coverage_misc() {
    test_bad_file();
    test_bad_section();
    test_bad_comment();
    test_long_line();
    test_duplicate_sections();
}