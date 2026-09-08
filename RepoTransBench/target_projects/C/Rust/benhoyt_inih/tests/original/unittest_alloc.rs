//! Rust translation of tests/unittest_alloc.c
use benhoyt_inih_rust::*;
use std::cell::RefCell;
use std::any::Any;

thread_local! {
    static PREV_SECTION: RefCell<String> = RefCell::new(String::with_capacity(50));
}

fn ini_malloc(size: usize) -> *mut u8 {
    println!("ini_malloc({})", size);
    vec![0u8; size].into_boxed_slice().as_mut_ptr()
}
fn ini_free(_ptr: *mut u8) {
    println!("ini_free()");
    // do nothing (Rust box drops on scope end)
}
fn ini_realloc(_ptr: *mut u8, size: usize) -> *mut u8 {
    println!("ini_realloc({})", size);
    vec![0u8; size].into_boxed_slice().as_mut_ptr()
}

// Handler for dumping section/name/value.
fn dumper(_user: &mut (), section: &str, name: Option<&str>, value: Option<&str>, _lineno: Option<usize>) -> i32 {
    PREV_SECTION.with(|prev| {
        let mut prev = prev.borrow_mut();
        if let Some(name) = name {
            if section != prev.as_str() {
                println!("... [{}]", section);
                *prev = section.to_string();
            }
            println!("... {}={};", name, value.unwrap_or(""));
        }
    });
    1
}

fn parse(name: &str, string: &str) {
    PREV_SECTION.with(|prev| prev.borrow_mut().clear());
    let mut user = ();
    let e = ini_parse_string(string, &mut |section, name, value, lineno| {
        dumper(&mut user, section, Some(name), value, lineno)
    }, &mut user as &mut dyn Any);
    println!("{}: e={}", name, e);
}

#[test]
fn test_custom_allocator() {
    parse("basic", "[section]\nfoo = bar\nbazz = buzz quxx");
}