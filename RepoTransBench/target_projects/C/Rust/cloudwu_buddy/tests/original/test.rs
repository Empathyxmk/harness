//! Translation of test.c for the cloudwu_buddy package in Rust

use cloudwu_buddy::*;

fn test_alloc(b: &mut Buddy, sz: usize) -> i32 {
    let r = buddy_alloc(b, sz);
    println!("alloc {} (sz= {})", r, sz);
    buddy_dump(b);
    r
}

fn test_free(b: &mut Buddy, addr: i32) {
    println!("free {}", addr);
    buddy_free(b, addr);
    buddy_dump(b);
}

fn test_size(b: &Buddy, addr: i32) {
    let s = buddy_size(b, addr);
    println!("size {} (sz = {})", addr, s);
}

#[test]
fn test_main() {
    let mut b = buddy_new(5);
    buddy_dump(&b);
    let m1 = test_alloc(&mut b, 4);
    test_size(&b, m1);
    let m2 = test_alloc(&mut b, 9);
    test_size(&b, m2);
    let m3 = test_alloc(&mut b, 3);
    test_size(&b, m3);
    let m4 = test_alloc(&mut b, 7);
    test_free(&mut b, m3);
    test_free(&mut b, m1);
    test_free(&mut b, m4);
    test_free(&mut b, m2);

    let m5 = test_alloc(&mut b, 32);
    test_free(&mut b, m5);

    let m6 = test_alloc(&mut b, 0);
    test_free(&mut b, m6);

    buddy_delete(b);
}