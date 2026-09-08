//! Translation of test_edgecases.c for the cloudwu_buddy package in Rust

use cloudwu_buddy::*;

#[test]
fn test_full_alloc_then_fail() {
    let mut b = buddy_new(2); // size 4
    let r1 = buddy_alloc(&mut b, 1);
    let r2 = buddy_alloc(&mut b, 1);
    let r3 = buddy_alloc(&mut b, 1);
    let r4 = buddy_alloc(&mut b, 1);
    assert!(r1 >= 0 && r2 >= 0 && r3 >= 0 && r4 >= 0);
    let fail = buddy_alloc(&mut b, 1);
    assert_eq!(fail, -1);
    buddy_free(&mut b, r1);
    buddy_free(&mut b, r2);
    buddy_free(&mut b, r3);
    buddy_free(&mut b, r4);
    buddy_delete(b);
}

#[test]
fn test_fragmented_fail_large_request() {
    let mut b = buddy_new(3); // size 8
    let mut r = [0; 4];
    for i in 0..4 { r[i] = buddy_alloc(&mut b, 2); }
    buddy_free(&mut b, r[1]);
    buddy_free(&mut b, r[2]);
    let fail = buddy_alloc(&mut b, 4);
    assert_eq!(fail, -1);
    buddy_free(&mut b, r[0]);
    buddy_free(&mut b, r[3]);
    buddy_delete(b);
}

#[test]
fn test_fullcycle_largest_block() {
    let mut b = buddy_new(5); // size 32
    let r = buddy_alloc(&mut b, 32);
    assert_eq!(r, 0);
    buddy_free(&mut b, r);
    buddy_delete(b);
}

#[test]
fn test_reuse_after_free() {
    let mut b = buddy_new(1); // size 2
    let r1 = buddy_alloc(&mut b, 1);
    assert_eq!(r1, 0);
    buddy_free(&mut b, r1);
    let r2 = buddy_alloc(&mut b, 2);
    assert_eq!(r2, 0);
    buddy_free(&mut b, r2);
    buddy_delete(b);
}