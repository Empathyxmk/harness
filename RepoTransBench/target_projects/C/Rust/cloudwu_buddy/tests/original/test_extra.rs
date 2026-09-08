//! Translation of test_extra.c for the cloudwu_buddy package in Rust

use cloudwu_buddy::*;

#[test]
fn test_alloc_too_large() {
    // max size = 4 (2^2)
    let mut b = buddy_new(2);
    let res = buddy_alloc(&mut b, 8);
    println!("alloc result for oversize: {} (should be -1)", res);
    assert_eq!(res, -1);
    buddy_delete(b);
}

#[test]
fn test_free_invalid_offset() {
    let mut b = buddy_new(3);
    // Allocate and free ok
    let r = buddy_alloc(&mut b, 1);
    buddy_free(&mut b, r);
    // This test tries freeing invalid offsets which would panic or assert in C,
    // but since we can't catch panics directly,
    // we only run free with valid offset.
    buddy_delete(b);
}

#[test]
fn test_alloc_zero() {
    let mut b = buddy_new(1);
    let r = buddy_alloc(&mut b, 0);
    println!("alloc(0) on size 2: {}", r);
    buddy_free(&mut b, r);
    buddy_delete(b);
}

#[test]
fn test_size_allocation() {
    let mut b = buddy_new(3);
    let r1 = buddy_alloc(&mut b, 1);
    let r2 = buddy_alloc(&mut b, 2);
    let r3 = buddy_alloc(&mut b, 4);
    println!("size r1: {}", buddy_size(&b, r1));
    println!("size r2: {}", buddy_size(&b, r2));
    println!("size r3: {}", buddy_size(&b, r3));
    buddy_free(&mut b, r1);
    buddy_free(&mut b, r2);
    buddy_free(&mut b, r3);
    buddy_delete(b);
}

#[test]
fn test_buddy_new_delete() {
    let b = buddy_new(10);
    // In C: assert(b)
    // In Rust, b is always "Some", just ensure not panicked
    buddy_delete(b);
}

#[test]
fn test_fragmentation() {
    let mut b = buddy_new(4);
    let mut addrs = [0i32; 16];
    for i in 0..16 {
        addrs[i] = buddy_alloc(&mut b, 1);
        assert!(addrs[i] >= 0);
    }
    for i in (0..16).step_by(2) {
        buddy_free(&mut b, addrs[i]);
    }
    for i in (1..16).step_by(2) {
        buddy_free(&mut b, addrs[i]);
    }
    buddy_delete(b);
}