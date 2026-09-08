//! Rust translation of tests/unittest_public_string.c
use benhoyt_inih_rust::*;
use std::cell::RefCell;

thread_local! {
    static PUB_USER: std::cell::RefCell<i32> = std::cell::RefCell::new(0);
    static PREV_SECTION_PUBLIC: RefCell<String> = RefCell::new(String::with_capacity(50));
}

fn dumper_public(user: &mut i32, section: &str, name: Option<&str>, value: Option<&str>, _lineno: Option<usize>) -> i32 {
    *user = *user;
    PREV_SECTION_PUBLIC.with(|prev| {
        let mut prev = prev.borrow_mut();
        if section != prev.as_str() {
            println!("[pubs] ... [{}]", section);
            *prev = section.to_string();
        }
        if let (Some(name), Some(val)) = (name, value) {
            println!("[pubs] ... {}={};", name, val);
        }
    });
    1
}

fn parse_public(name: &str, s: &str) {
    static mut U: i32 = 200;
    PREV_SECTION_PUBLIC.with(|prev| prev.borrow_mut().clear());
    let mut user = 0;
    let e = ini_parse_string(s, &mut |section, name, value, _| dumper_public(&mut user, section, Some(name), value, None), &mut user);
    println!("{}: e={} user={}", name, e, user);
    unsafe { U += 1; }
}

#[test]
fn test_public_string_cases() {
    parse_public("pub_empty string", "");
    parse_public("pub_simple", "[alpha]\nkey1 = foo\nkey2 = bar baz");
    parse_public("pub_cr", "[beta]\rkeyA = world\rkeyB = 24\r");
    parse_public("pub_publine", "[mine]\nx = abcdefghijklmnopqrst\nb=1234\n");
    parse_public("pub_error2", "[p]\ny=2\nq\nz=9");
}