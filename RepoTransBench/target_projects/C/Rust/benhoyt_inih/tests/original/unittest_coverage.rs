//! Rust translation of tests/unittest_coverage.c
use benhoyt_inih_rust::*;

#[derive(Default)]
struct IniParseOptions {
    allow_multi_line: bool,
    allow_bom: bool,
    allow_inline_comments: bool,
    allow_no_value: bool,
    call_handler_on_new_section: bool,
}

fn fail_on_line3(called: &mut i32, _section: &str, _name: Option<&str>, _value: Option<&str>, _lineno: Option<usize>) -> i32 {
    *called += 1;
    if *called == 3 {
        return 0;
    }
    1
}

fn handler_print(_user: &mut (), section: &str, name: Option<&str>, value: Option<&str>, _lineno: Option<usize>) -> i32 {
    println!("Section: {}, Name: {}, Value: {}", section, name.unwrap_or(""), value.unwrap_or("(null)"));
    1
}

fn test_stop_on_first_error() {
    let mut called = 0;
    let res = ini_parse("normal.ini", &mut |sec, name, val, lin| fail_on_line3(&mut called, sec, Some(name), val, lin), &mut called as &mut dyn std::any::Any);
    println!("test_stop_on_first_error: result={}, called={}", res, called);
}

fn test_disallow_inline_comments() {
    let opts = IniParseOptions {
        allow_inline_comments: false,
        ..Default::default()
    };
    ini_parse_with_options("normal.ini", &mut |sec, name, val, _| handler_print(&mut (), sec, Some(name), val, None), &mut (), &opts);
    println!("test_disallow_inline_comments: done");
}

fn test_call_handler_on_new_section() {
    let opts = IniParseOptions {
        call_handler_on_new_section: true,
        ..Default::default()
    };
    ini_parse_with_options("normal.ini", &mut |sec, name, val, _| handler_print(&mut (), sec, Some(name), val, None), &mut (), &opts);
    println!("test_call_handler_on_new_section: done");
}

fn test_allow_no_value() {
    let opts = IniParseOptions {
        allow_no_value: true,
        ..Default::default()
    };
    ini_parse_with_options("no_value.ini", &mut |sec, name, val, _| handler_print(&mut (), sec, Some(name), val, None), &mut (), &opts);
    println!("test_allow_no_value: done");
}

fn test_disable_multiline() {
    let opts = IniParseOptions {
        allow_multi_line: false,
        ..Default::default()
    };
    ini_parse_with_options("multi_line.ini", &mut |sec, name, val, _| handler_print(&mut (), sec, Some(name), val, None), &mut (), &opts);
    println!("test_disable_multiline: done");
}

#[test]
fn full_coverage_runs() {
    test_stop_on_first_error();
    test_disallow_inline_comments();
    test_call_handler_on_new_section();
    test_allow_no_value();
    test_disable_multiline();
}