//! Rust translation of tests/unittest_string.c
use benhoyt_inih_rust::*;
use std::cell::RefCell;
use std::any::Any;

thread_local! {
    static USER: RefCell<i32> = RefCell::new(0);
    static PREV_SECTION: RefCell<String> = RefCell::new(String::with_capacity(50));
}

fn dumper(user: &mut i32, section: &str, name: Option<&str>, value: Option<&str>, _lineno: Option<usize>) -> i32 {
    *user = *user;
    PREV_SECTION.with(|prev| {
        let mut prev = prev.borrow_mut();
        if section != prev.as_str() {
            println!("... [{}]", section);
            *prev = section.to_string();
        }
        if let (Some(name), Some(val)) = (name, value) {
            println!("... {}={};", name, val);
        }
    });
    1
}

fn parse(name: &str, s: &str) {
    static mut U: i32 = 100;
    PREV_SECTION.with(|prev| prev.borrow_mut().clear());
    let mut user = 0;
    let e = ini_parse_string(s, &mut |section, name, value, _| {
        dumper(&mut user, section, Some(name), value, None)
    }, &mut user as &mut dyn Any);
    println!("{}: e={} user={}", name, e, user);
    unsafe { U += 1; }
}

#[test]
fn test_string_parse_variants() {
    parse("empty string", "");
    parse("basic", "[section]\nfoo = bar\nbazz = buzz quxx");
    parse("crlf", "[section]\r\nhello = world\r\nforty_two = 42\r\n");
    parse("long line", "[sec]\nfoo = 01234567890123456789\nbar=4321\n");
    parse("long continued", "[sec]\nfoo = 0123456789012bix=1234\n");
    parse("error", "[s]\na=1\nb\nc=3");
}