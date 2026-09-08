// Translated from test/public_test_vec.c (public tests)
use rxi_vec::{VecInt, VecDouble};

macro_rules! my_assert {
    ($cond:expr) => {
        if !$cond {
            panic!("[FAIL] {}:{}: {}", file!(), line!(), stringify!($cond));
        }
    };
}

#[test]
fn test_vec_push_public() {
    let mut v = VecInt::new();
    for i in 0..777 {
        v.push(i * 3);
    }
    my_assert!(v.data[2] == 6);
    my_assert!(v.data[776] == 776 * 3);
    my_assert!(v.push(23) == 0);
}

#[test]
fn test_vec_pop_public() {
    let mut v = VecInt::new();
    v.push(234);
    v.push(876);
    v.push(432);
    my_assert!(v.pop() == 432);
    my_assert!(v.pop() == 876);
    my_assert!(v.pop() == 234);
}

#[test]
fn test_vec_splice_public() {
    let mut v = VecInt::new();
    for i in 0..777 { v.push(i + 5); }
    v.splice(0, 9);
    my_assert!(v.data[0] == 14);
    my_assert!(v.data[10] == 24);
    my_assert!(v.data[v.len() - 1] == 781);
}

#[test]
fn test_vec_swapsplice_public() {
    let mut v = VecInt::new();
    for i in 0..10 { v.push(i + 50); }
    v.swapsplice(0, 7);
    my_assert!(v.data[0] == 57 && v.data[1] == 58 && v.data[2] == 59);
    my_assert!(v.data[v.len() - 1] == 56);
}

#[test]
fn test_vec_insert_public() {
    let mut v = VecInt::new();
    for i in 0..333 { v.insert(0, i + 5); }
    my_assert!(v.data[0] == 333 + 4);
    my_assert!(v.data[v.len() - 1] == 5);
    my_assert!(v.insert(15, 456) == 0);
    my_assert!(v.data[15] == 456);
    my_assert!(v.len() == 334);
    v.insert(v.len() - 2, 322);
    my_assert!(v.data[v.len() - 3] == 322);
    v.insert(v.len(), 678);
    my_assert!(v.data[v.len() - 1] == 678);
}

#[test]
fn test_vec_sort_public() {
    let mut v = VecInt::new();
    let arr = [8, 7, 19, 0, -3, 10];
    for x in &arr { v.push(*x); }
    v.data.sort();
    my_assert!(v.data[0] == -3);
    my_assert!(v.data[1] == 0);
    my_assert!(v.data[2] == 7);
}

#[test]
fn test_vec_swap_public() {
    let mut v = VecInt::new();
    v.push('x' as i32); v.push('y' as i32); v.push('z' as i32);
    v.swap(0, 2);
    my_assert!(v.data[0] == 'z' as i32 && v.data[2] == 'x' as i32);
    v.swap(0, 1);
    my_assert!(v.data[0] == 'y' as i32 && v.data[1] == 'z' as i32);
    v.swap(1, 2);
    my_assert!(v.data[1] == 'x' as i32 && v.data[2] == 'z' as i32);
    v.swap(1, 1);
    my_assert!(v.data[1] == 'x' as i32);
}

#[test]
fn test_vec_truncate_public() {
    let mut v = VecInt::new();
    for i in 0..777 { v.push(i); }
    my_assert!(v.len() == 777);
    v.truncate(700);
    my_assert!(v.len() == 700);
}

#[test]
fn test_vec_clear_public() {
    let mut v = VecInt::new();
    for i in 0..123 { v.push(i); }
    v.clear();
    my_assert!(v.len() == 0);
}

#[test]
fn test_vec_first_public() {
    let mut v = VecInt::new();
    v.push(0xbaad);
    my_assert!(v.first() == 0xbaad);
}

#[test]
fn test_vec_last_public() {
    let mut v = VecInt::new();
    v.push(999_999);
    my_assert!(v.last() == 999_999);
}

#[test]
fn test_vec_reserve_public() {
    let mut v = VecInt::new();
    v.reserve(52);
    my_assert!(v.capacity() >= 52);
    v.reserve(25);
    my_assert!(v.capacity() >= 52);
    let mut v2 = VecInt::new();
    v2.reserve(104);
    my_assert!(v2.capacity() >= 104);
    my_assert!(v2.reserve(300) == 0);
}

#[test]
fn test_vec_compact_public() {
    let mut v = VecInt::new();
    for i in 0..20 { v.push(i + 15); }
    v.reserve(32);
    v.compact();
    my_assert!(v.len() == v.capacity());
    my_assert!(v.compact() == 0);
}

#[test]
fn test_vec_pusharr_public() {
    let arr = [7,8,9,10,11,12,13];
    let mut v = VecInt::new();
    v.pusharr(&arr);
    my_assert!(v.data[0] == 7);
    my_assert!(v.data[2] == 9);
    my_assert!(v.data[6] == 13);
    let arr2 = [15,16,17];
    v.clear();
    v.pusharr(&arr2);
    my_assert!(v.data[0] == 15);
}

#[test]
fn test_vec_extend_public() {
    let mut a = VecInt::new();
    let mut b = VecInt::new();
    let arr = [22,44];
    a.pusharr(&arr);
    let arr2 = [77,99];
    b.pusharr(&arr2);
    a.extend(&b);
    my_assert!(a.data[0] == 22 && a.data[1] == 44 && a.data[2] == 77 && a.data[3] == 99);
    my_assert!(a.len() == 4);
}

#[test]
fn test_vec_find_public() {
    let mut v = VecInt::new();
    for i in 100..126 { v.push(i); }
    let mut i = v.find(100);
    my_assert!(i == 0);
    i = v.find(125);
    my_assert!(i == 25);
    v.push(500);
    i = v.find(500);
    my_assert!(i == 26);
    i = v.find(-999);
    my_assert!(i == -1);
}

#[test]
fn test_vec_remove_public() {
    let mut v = VecInt::new();
    for i in 0..26 { v.push('z' as i32 - i); }
    my_assert!(v.len() == 26);
    v.remove(25);
    my_assert!(v.len() == 25);
}

#[test]
fn test_vec_reverse_public() {
    let mut v = VecInt::new();
    v.push('w' as i32);
    v.push('x' as i32);
    v.push('y' as i32);
    v.push('z' as i32);
    v.reverse();
    my_assert!(v.len() == 4);
    my_assert!(v.data[0] == 'z' as i32 && v.data[1] == 'y' as i32 && v.data[2] == 'x' as i32 && v.data[3] == 'w' as i32);
}

#[test]
fn test_vec_foreach_public() {
    let mut v = VecInt::new();
    v.push(4); v.push(9); v.push(16);
    let mut acc = 1;
    for (i, &val) in v.data.iter().enumerate() {
        acc *= val + i as i32;
    }
    my_assert!(acc == (4 + 0) * (9 + 1) * (16 + 2));
}

#[test]
fn test_vec_foreach_rev_public() {
    let mut v = VecInt::new();
    v.push(4); v.push(9); v.push(16);
    let mut vals: Vec<i32> = v.data.iter().cloned().collect();
    vals.reverse();
    let mut acc = 1;
    for (i, &val) in vals.iter().enumerate() {
        acc *= val + i as i32;
    }
    my_assert!(acc == (4 + 2) * (9 + 1) * (16 + 0));
}

#[test]
fn test_vec_foreach_ptr_public() {
    let mut v = VecInt::new();
    v.push(4); v.push(9); v.push(16);
    let mut acc = 1;
    for (i, val) in v.data.iter().enumerate() {
        acc *= *val + i as i32;
    }
    my_assert!(acc == (4 + 0) * (9 + 1) * (16 + 2));
}

#[test]
fn test_vec_foreach_ptr_rev_public() {
    let mut v = VecInt::new();
    v.push(4); v.push(9); v.push(16);
    let mut vals: Vec<i32> = v.data.iter().cloned().collect();
    vals.reverse();
    let mut acc = 1;
    for (i, val) in vals.iter().enumerate() {
        acc *= *val + i as i32;
    }
    my_assert!(acc == (4 + 2) * (9 + 1) * (16 + 0));
}