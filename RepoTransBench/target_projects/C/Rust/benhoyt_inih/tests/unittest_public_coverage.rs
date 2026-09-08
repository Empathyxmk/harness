//! Rust translation of tests/unittest_public_coverage.c
use benhoyt_inih_rust::*;

#[derive(Default)]
struct IniParseOptions {
    allow_multi_line: bool,
    allow_bom: bool,
    allow_inline_comments: bool,
    allow_no_value: bool,
    call_handler_on_new_section: bool,
}

fn fail_on_line2(called: &mut i32, _section: &str, _name: Option<&str>, _value: Option<&str>, _lineno: Option<usize>) -> i32 {
    *called += 1;
    if *called == 2 {
        return 0;
    }
    1
}

fn handler_print_public(_user: &mut (), section: &str, name: Option<&str>, value: Option<&str>, _lineno: Option<usize>) -> i32 {
    println!("[P] Section: {}, Name: {}, Value: {}", section, name.unwrap_or(""), value.unwrap_or("(null)"));
    1
}

fn test_stop_on_first_error_public() {
    let mut called = 0;
    let res = ini_parse("baseline_single.txt", &mut |sec, name, val, lin| fail_on_line2(&mut called, sec, Some(name), val, lin), &mut called as &mut dyn std::any::Any);
    println!("test_public_stop_on_first_error: result={}, called={}", res, called);
}
fn test_disallow_inline_comments_public() {
    let opts = IniParseOptions {
        allow_inline_comments: false,
        ..Default::default()
    };
    ini_parse_with_options("baseline_string.txt", &mut |sec, name, val, _| handler_print_public(&mut (), sec, Some(name), val, None), &mut (), &opts);
    println!("test_public_disallow_inline_comments: done");
}
fn test_call_handler_on_new_section_public() {
    let opts = IniParseOptions {
        call_handler_on_new_section: true,
        ..Default::default()
    };
    ini_parse_with_options("baseline_multi.txt", &mut |sec, name, val, _| handler_print_public(&mut (), sec, Some(name), val, None), &mut (), &opts);
    println!("test_public_call_handler_on_new_section: done");
}
fn test_allow_no_value_public() {
    let opts = IniParseOptions {
        allow_no_value: true,
        ..Default::default()
    };
    ini_parse_with_options("no_value.ini", &mut |sec, name, val, _| handler_print_public(&mut (), sec, Some(name), val, None), &mut (), &opts);
    println!("test_public_allow_no_value: done");
}
fn test_disable_multiline_public() {
    let opts = IniParseOptions {
        allow_multi_line: false,
        ..Default::default()
    };
    ini_parse_with_options("baseline_multi_max_line.txt", &mut |sec, name, val, _| handler_print_public(&mut (), sec, Some(name), val, None), &mut (), &opts);
    println!("test_public_disable_multiline: done");
}

#[test]
fn public_coverage() {
    test_stop_on_first_error_public();
    test_disallow_inline_comments_public();
    test_call_handler_on_new_section_public();
    test_allow_no_value_public();
    test_disable_multiline_public();
}