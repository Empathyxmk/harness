//! Rust translation of tests/unittest.c
use benhoyt_inih_rust::*;
use std::cell::RefCell;
use std::any::Any;
use std::fs;

thread_local! {
    static USER: RefCell<i32> = RefCell::new(0);
    static PREV_SECTION: RefCell<String> = RefCell::new(String::with_capacity(50));
}

// Dummy implementation of the handler. The real parser should call this for each (section, name, value).
fn dumper(user: &mut i32, section: &str, name: Option<&str>, value: Option<&str>, lineno: Option<usize>) -> i32 {
    *user = *user;
    PREV_SECTION.with(|prev| {
        let mut prev = prev.borrow_mut();
        if name.is_none() || section != prev.as_str() {
            println!("... [{}]", section);
            *prev = section.to_string();
        }
        if let Some(name) = name {
            let value_part = if let Some(v) = value { format!("={}", v) } else { String::new() };
            if let Some(lineno) = lineno {
                println!("... {}{};  line {}", name, value_part, lineno);
            } else {
                println!("... {}{};", name, value_part);
            }
        }
    });
    if name.is_none() {
        // No name provided, likely due to INI_ALLOW_NO_VALUE
        return 1;
    }
    if value.is_none() {
        return 1;
    }
    if let (Some("user"), Some("parse_error")) = (name, value) {
        0
    } else {
        1
    }
}

fn parse(fname: &str) {
    let mut user_val = 100;
    PREV_SECTION.with(|prev| prev.borrow_mut().clear());
    // You'd pass the actual dumper handler through; here we just pretend.
    let e = ini_parse(fname, &mut |section, name, value, lineno| {
        dumper(&mut user_val, section, Some(name), value, lineno)
    }, &mut user_val as &mut dyn Any);
    println!("{}: e={} user={}", fname, e, user_val);
}

#[test]
fn test_original_set() {
    parse("no_file.ini");
    parse("normal.ini");
    parse("bad_section.ini");
    parse("bad_comment.ini");
    parse("user_error.ini");
    parse("multi_line.ini");
    parse("bad_multi.ini");
    parse("bom.ini");
    parse("duplicate_sections.ini");
    parse("no_value.ini");
    parse("long_section.ini");
    parse("long_line.ini");
}