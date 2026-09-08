//! Rust translation of tests/unittest_public_alloc.c
use benhoyt_inih_rust::*;
use std::cell::RefCell;

thread_local! {
    static PREV_SECTION_PUBLIC: RefCell<String> = RefCell::new(String::with_capacity(50));
}

fn ini_malloc(size: usize) -> *mut u8 {
    println!("[pub] ini_malloc({})", size);
    vec![0u8; size].into_boxed_slice().as_mut_ptr()
}
fn ini_free(_ptr: *mut u8) {
    println!("[pub] ini_free()");
}
fn ini_realloc(_ptr: *mut u8, size: usize) -> *mut u8 {
    println!("[pub] ini_realloc({})", size);
    vec![0u8; size].into_boxed_slice().as_mut_ptr()
}
fn dumper_public(_user: &mut (), section: &str, name: Option<&str>, value: Option<&str>, _lineno: Option<usize>) -> i32 {
    PREV_SECTION_PUBLIC.with(|prev| {
        let mut prev = prev.borrow_mut();
        if let Some(name) = name {
            if section != prev.as_str() {
                println!("[pub] ... [{}]", section);
                *prev = section.to_string();
            }
            println!("[pub] ... {}={};", name, value.unwrap_or(""));
        }
    });
    1
}
fn parse_public(name: &str, string: &str) {
    PREV_SECTION_PUBLIC.with(|prev| prev.borrow_mut().clear());
    let mut user = ();
    let e = ini_parse_string(string, &mut |section, name, value, _| dumper_public(&mut user, section, Some(name), value, None), &mut user);
    println!("{}: e={}", name, e);
}

#[test]
fn test_public_custom_alloc() {
    parse_public("pub_basic", "[foo]\nalice=1\nbob=2");
}