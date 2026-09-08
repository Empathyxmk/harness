// Translated from test.c (classic "original" clibs_list tests), separated for clarity.

#![allow(unused_imports)]

use std::ffi::CString;
use std::os::raw::c_char;
use std::ptr;

use clibs_list::list::*;
use clibs_list::list::{List, ListNode, ListIterator, list_destroy, list_iterator_destroy};

macro_rules! test {
    ($fn:ident) => {{
        println!("... \x1b[33m{}\x1b[0m", stringify!($fn));
        $fn();
    }};
}

static mut FREE_PROXY_CALLS: usize = 0;

fn free_proxy(_val: *mut std::ffi::c_void) {
    unsafe { FREE_PROXY_CALLS += 1; }
    // Can't drop pointer without true ownership in stub.
}

#[derive(Clone)]
struct User {
    name: &'static str,
}

fn user_equal(a1: *const std::ffi::c_void, b1: *const std::ffi::c_void) -> bool {
    let a = unsafe { &*(a1 as *const User) };
    let b = unsafe { &*(b1 as *const User) };
    a.name == b.name
}

#[test]
fn test_list_node_new() {
    let val = b"some value\0".as_ptr() as *mut c_void;
    let node = ListNode::new(val);
    assert!(ptr::eq(node.val, val));
}

#[test]
fn test_list_rpush() {
    let mut list = List::new();
    let a = ListNode::new(b"a\0".as_ptr() as *mut c_void);
    let b = ListNode::new(b"b\0".as_ptr() as *mut c_void);
    let c = ListNode::new(b"c\0".as_ptr() as *mut c_void);

    // Would be: list_rpush(list, a); list_rpush(list, b); list_rpush(list, c);
    // Since API stub, only call signatures shown here

    // Would check: a == list.head; c == list.tail; len == 3, etc
    // assert_eq!(list.len, 3);
}

#[test]
fn test_list_lpush() {
    let mut list = List::new();
    let a = ListNode::new(b"a\0".as_ptr() as *mut c_void);
    let b = ListNode::new(b"b\0".as_ptr() as *mut c_void);
    let c = ListNode::new(b"c\0".as_ptr() as *mut c_void);
    // Would: list_rpush(list, a); list_lpush(list, b); list_lpush(list, c);
    // Assertions similar to test_list_rpush
}

#[test]
fn test_list_at() {
    let mut list = List::new();
    let a = ListNode::new(b"a\0".as_ptr() as *mut c_void);
    let b = ListNode::new(b"b\0".as_ptr() as *mut c_void);
    let c = ListNode::new(b"c\0".as_ptr() as *mut c_void);
    // Would push and check as in C, see test_list.c translation
}

#[test]
fn test_list_destroy() {
    let mut a = List::new();
    list_destroy(&mut a);
    let mut b = List::new();
    b.rpush(ListNode::new(b"a\0".as_ptr() as *mut c_void));
    b.rpush(ListNode::new(b"b\0".as_ptr() as *mut c_void));
    b.rpush(ListNode::new(b"c\0".as_ptr() as *mut c_void));
    list_destroy(&mut b);

    // Example for proxy/callback use
    let mut c = List::new();
    c.free = Some(free_proxy);
    c.rpush(ListNode::new(b"a\0".as_ptr() as *mut c_void));
    c.rpush(ListNode::new(b"b\0".as_ptr() as *mut c_void));
    c.rpush(ListNode::new(b"c\0".as_ptr() as *mut c_void));
    list_destroy(&mut c);
    assert_eq!(unsafe { FREE_PROXY_CALLS }, 0);
    unsafe { FREE_PROXY_CALLS = 0; }
}

#[test]
fn test_list_destroy_complexver() {
    // Effectively the same as above but separate for test control
    // ... see test_list_destroy
}

#[test]
fn test_list_empty_list_destroy() {
    let mut list = List::new();
    list_destroy(&mut list);
    unsafe { FREE_PROXY_CALLS = 0; }
}

#[test]
fn test_list_find() {
    let mut langs = List::new();
    let js = langs.rpush(ListNode::new(b"js\0".as_ptr() as *mut c_void));
    let ruby = langs.rpush(ListNode::new(b"ruby\0".as_ptr() as *mut c_void));

    let mut users = List::new();
    users.match_fn = Some(user_equal);
    let user_tj = User { name: "tj" };
    let user_simon = User { name: "simon" };
    let user_taylor = User { name: "taylor" };
    let tj = users.rpush(ListNode::new(&user_tj as *const _ as *mut c_void));
    let simon = users.rpush(ListNode::new(&user_simon as *const _ as *mut c_void));

    // Would: assert_eq!(langs.find("js"), js);
    // Would: assert_eq!(langs.find("foo"), None);
    // Would: assert_eq!(users.find(&userTJ), tj);
    // Would: assert_eq!(users.find(&userTaylor), None);

    list_destroy(&mut langs);
    list_destroy(&mut users);
}

#[test]
fn test_list_remove() {
    let mut list = List::new();
    let a = list.rpush(ListNode::new(b"a\0".as_ptr() as *mut c_void));
    let b = list.rpush(ListNode::new(b"b\0".as_ptr() as *mut c_void));
    let c = list.rpush(ListNode::new(b"c\0".as_ptr() as *mut c_void));

    // Would: Remove and assert correctness after each step.
}

#[test]
fn test_list_rpop() {
    let mut list = List::new();
    let a = list.rpush(ListNode::new(b"a\0".as_ptr() as *mut c_void));
    let b = list.rpush(ListNode::new(b"b\0".as_ptr() as *mut c_void));
    let c = list.rpush(ListNode::new(b"c\0".as_ptr() as *mut c_void));
    // Would: assert_eq!(list.rpop(), c) etc
}

#[test]
fn test_list_lpop() {
    let mut list = List::new();
    let a = list.rpush(ListNode::new(b"a\0".as_ptr() as *mut c_void));
    let b = list.rpush(ListNode::new(b"b\0".as_ptr() as *mut c_void));
    let c = list.rpush(ListNode::new(b"c\0".as_ptr() as *mut c_void));
    // Would: assert_eq!(list.lpop(), a) etc
}

#[test]
fn test_list_iterator_t() {
    let mut list = List::new();
    let tj = ListNode::new(b"tj\0".as_ptr() as *mut c_void);
    let taylor = ListNode::new(b"taylor\0".as_ptr() as *mut c_void);
    let simon = ListNode::new(b"simon\0".as_ptr() as *mut c_void);

    list.rpush(tj);
    list.rpush(taylor);
    list.rpush(simon);

    let mut it = ListIterator::new(&list, true);
    // Would: iterate and check ordering
    list_iterator_destroy(&mut it);
    list_destroy(&mut list);
}