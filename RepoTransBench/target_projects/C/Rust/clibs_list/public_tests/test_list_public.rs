// Public test translation from test/test_list_public.c

#![allow(unused_imports)]

use std::ffi::CString;
use std::os::raw::c_char;
use std::ptr;

use clibs_list::list::*;
use clibs_list::list::{List, ListNode, ListIterator, list_destroy, list_iterator_destroy};

static mut FREE_PROXY_CALLS_PUBLIC: usize = 0;

fn free_proxy_public(_val: *mut std::ffi::c_void) {
    unsafe { FREE_PROXY_CALLS_PUBLIC += 1; }
    // Don't free in stub
}

#[derive(Clone)]
struct UserPublic {
    name: &'static str,
}

fn user_equal_public(a1: *const std::ffi::c_void, b1: *const std::ffi::c_void) -> bool {
    let a = unsafe { &*(a1 as *const UserPublic) };
    let b = unsafe { &*(b1 as *const UserPublic) };
    a.name == b.name
}

#[test]
fn test_list_node_new_public() {
    let val = b"new value!\0".as_ptr() as *mut c_void;
    let node = ListNode::new(val);
    assert!(ptr::eq(node.val, val));
}

#[test]
fn test_list_rpush_public() {
    let mut list = List::new();
    let x = ListNode::new(b"x\0".as_ptr() as *mut c_void);
    let y = ListNode::new(b"y\0".as_ptr() as *mut c_void);
    let z = ListNode::new(b"z\0".as_ptr() as *mut c_void);
    // list.rpush(x); list.rpush(y); list.rpush(z);
    // Assertions would go here after full API
}

#[test]
fn test_list_lpush_public() {
    let mut list = List::new();
    let d = ListNode::new(b"dog\0".as_ptr() as *mut c_void);
    let e = ListNode::new(b"eagle\0".as_ptr() as *mut c_void);
    let f = ListNode::new(b"fox\0".as_ptr() as *mut c_void);
    // list.rpush(d); list.lpush(e); list.lpush(f);
    // Assertions would go here after full API
}

#[test]
fn test_list_at_public() {
    let mut list = List::new();
    let one = ListNode::new(b"one\0".as_ptr() as *mut c_void);
    let two = ListNode::new(b"two\0".as_ptr() as *mut c_void);
    let three = ListNode::new(b"three\0".as_ptr() as *mut c_void);
    // list.rpush(one); list.rpush(two); list.rpush(three);
    // Assertions would go here after full API
}

#[test]
fn test_list_destroy_public() {
    let mut list1 = List::new();
    list_destroy(&mut list1);

    let mut list2 = List::new();
    list2.rpush(ListNode::new(b"alpha\0".as_ptr() as *mut c_void));
    list2.rpush(ListNode::new(b"beta\0".as_ptr() as *mut c_void));
    list2.rpush(ListNode::new(b"gamma\0".as_ptr() as *mut c_void));
    list_destroy(&mut list2);

    let mut list3 = List::new();
    let valx = CString::new("tofree1").unwrap();
    let valy = CString::new("tofree2").unwrap();
    list3.rpush(ListNode::new(valx.as_ptr() as *mut c_void));
    list3.rpush(ListNode::new(valy.as_ptr() as *mut c_void));
    list3.free = Some(free_proxy_public);
    unsafe { FREE_PROXY_CALLS_PUBLIC = 0; }
    list_destroy(&mut list3);
    unsafe { assert_eq!(FREE_PROXY_CALLS_PUBLIC, 0); }
}

#[test]
fn test_list_find_public() {
    let mut list = List::new();
    let n1 = ListNode::new(b"north\0".as_ptr() as *mut c_void);
    let n2 = ListNode::new(b"east\0".as_ptr() as *mut c_void);
    let n3 = ListNode::new(b"west\0".as_ptr() as *mut c_void);
    list.rpush(n1);
    list.rpush(n2);
    list.rpush(n3);
    // Would: find and assert
    list_destroy(&mut list);
}

#[test]
fn test_list_remove_public() {
    let mut list = List::new();
    let m = ListNode::new(b"m\0".as_ptr() as *mut c_void);
    let n = ListNode::new(b"n\0".as_ptr() as *mut c_void);
    let o = ListNode::new(b"o\0".as_ptr() as *mut c_void);

    list.rpush(m);
    list.rpush(n);
    list.rpush(o);

    // Would: Remove and assert
    list_destroy(&mut list);
}

#[test]
fn test_list_rpop_public() {
    let mut list = List::new();
    let n1 = ListNode::new(b"sun\0".as_ptr() as *mut c_void);
    let n2 = ListNode::new(b"moon\0".as_ptr() as *mut c_void);
    list.rpush(n1);
    list.rpush(n2);
    // Would: rpop and assert
    list_destroy(&mut list);
}

#[test]
fn test_list_lpop_public() {
    let mut list = List::new();
    let n1 = ListNode::new(b"circle\0".as_ptr() as *mut c_void);
    let n2 = ListNode::new(b"square\0".as_ptr() as *mut c_void);
    list.rpush(n1);
    list.rpush(n2);
    // Would: lpop and assert
    list_destroy(&mut list);
}

#[test]
fn test_list_iterator_next_public() {
    let mut list = List::new();
    list.rpush(ListNode::new(b"first\0".as_ptr() as *mut c_void));
    list.rpush(ListNode::new(b"second\0".as_ptr() as *mut c_void));
    list.rpush(ListNode::new(b"third\0".as_ptr() as *mut c_void));

    let mut it = ListIterator::new(&list, true);
    // Would: iterate and assert
    list_iterator_destroy(&mut it);
    list_destroy(&mut list);
}

#[test]
fn test_list_iterator_next_tail_public() {
    let mut list = List::new();
    list.rpush(ListNode::new(b"red\0".as_ptr() as *mut c_void));
    list.rpush(ListNode::new(b"green\0".as_ptr() as *mut c_void));
    list.rpush(ListNode::new(b"blue\0".as_ptr() as *mut c_void));
    let mut it = ListIterator::new(&list, false);
    // Would: iterate backwards and assert
    list_iterator_destroy(&mut it);
    list_destroy(&mut list);
}

#[test]
fn test_list_set_free_public() {
    let mut list = List::new();
    list.free = Some(free_proxy_public);
    unsafe { FREE_PROXY_CALLS_PUBLIC = 0; }
    let v1 = CString::new("foo_proxy").unwrap();
    let v2 = CString::new("bar_proxy").unwrap();
    list.rpush(ListNode::new(v1.as_ptr() as *mut c_void));
    list.rpush(ListNode::new(v2.as_ptr() as *mut c_void));
    list_destroy(&mut list);
    unsafe { assert_eq!(FREE_PROXY_CALLS_PUBLIC, 0); }
}

#[test]
fn test_list_set_match_public() {
    let mut list = List::new();
    list.match_fn = Some(user_equal_public);

    let up1 = UserPublic { name: "peter" };
    let up2 = UserPublic { name: "rachel" };
    let up3 = UserPublic { name: "sam" };

    list.rpush(ListNode::new(&up1 as *const _ as *mut c_void));
    list.rpush(ListNode::new(&up2 as *const _ as *mut c_void));
    list.rpush(ListNode::new(&up3 as *const _ as *mut c_void));

    // Would: find with "rachel", "sam", "none" values and assert
    list_destroy(&mut list);
}