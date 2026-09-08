//! Translation of test_public.c for the cloudwu_buddy package in Rust (public test case)

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
fn test_public_patterns() {
    let mut b = buddy_new(4);

    buddy_dump(&b);

    let m1 = test_alloc(&mut b, 5);
    test_size(&b, m1);

    let m2 = test_alloc(&mut b, 7);
    test_size(&b, m2);

    let m3 = test_alloc(&mut b, 2);
    test_size(&b, m3);

    let m4 = test_alloc(&mut b, 8);
    test_free(&mut b, m2);
    test_free(&mut b, m4);
    test_free(&mut b, m1);
    test_free(&mut b, m3);

    let m5 = test_alloc(&mut b, 16);
    test_free(&mut b, m5);

    let m6 = test_alloc(&mut b, 1);
    test_free(&mut b, m6);

    buddy_delete(b);
}