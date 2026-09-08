// Translated from test/test_vec.c
use rxi_vec::{VecInt, VecDouble};

fn intptrcmp(a: &i32, b: &i32) -> std::cmp::Ordering {
    a.cmp(b)
}

#[test]
fn test_vec_push() {
    let mut v = VecInt::new();
    for i in 0..1000 {
        v.push(i * 2);
    }
    assert_eq!(v.data[1], 2);
    assert_eq!(v.data[999], 999 * 2);
    assert_eq!(v.push(10), 0);
}

#[test]
fn test_vec_pop() {
    let mut v = VecInt::new();
    v.push(123);
    v.push(456);
    v.push(789);
    assert_eq!(v.pop(), 789);
    assert_eq!(v.pop(), 456);
    assert_eq!(v.pop(), 123);
}

#[test]
fn test_vec_splice() {
    let mut v = VecInt::new();
    for i in 0..1000 {
        v.push(i);
    }
    v.splice(0, 10);
    assert_eq!(v.data[0], 10);
    v.splice(10, 10);
    assert_eq!(v.data[10], 30);
    let len = v.len();
    v.splice(len - 50, 50);
    assert_eq!(v.data[v.len() - 1], 949);
}

#[test]
fn test_vec_swapsplice() {
    let mut v = VecInt::new();
    for i in 0..10 {
        v.push(i);
    }
    v.swapsplice(0, 3);
    assert_eq!(v.data[0], 7);
    assert_eq!(v.data[1], 8);
    assert_eq!(v.data[2], 9);
    v.swapsplice(v.len() - 1, 1);
    assert_eq!(v.data[v.len() - 1], 5);
}

#[test]
fn test_vec_insert() {
    let mut v = VecInt::new();
    for i in 0..1000 {
        v.insert(0, i);
    }
    assert_eq!(v.data[0], 999);
    assert_eq!(v.data[v.len() - 1], 0);
    v.insert(10, 123);
    assert_eq!(v.data[10], 123);
    assert_eq!(v.len(), 1001);
    v.insert(v.len() - 2, 678);
    assert_eq!(v.data[999], 678);
    assert_eq!(v.insert(10, 123), 0);
    v.insert(v.len(), 789);
    assert_eq!(v.data[v.len() - 1], 789);
}

#[test]
fn test_vec_sort() {
    let mut v = VecInt::new();
    v.push(3);
    v.push(-1);
    v.push(0);
    v.data.sort_by(intptrcmp);
    assert_eq!(v.data[0], -1);
    assert_eq!(v.data[1], 0);
    assert_eq!(v.data[2], 3);
}

#[test]
fn test_vec_swap() {
    let mut v = VecInt::new();
    v.push('a' as i32);
    v.push('b' as i32);
    v.push('c' as i32);
    v.swap(0, 2);
    assert_eq!(v.data[0], 'c' as i32);
    assert_eq!(v.data[2], 'a' as i32);
    v.swap(0, 1);
    assert_eq!(v.data[0], 'b' as i32);
    assert_eq!(v.data[1], 'c' as i32);
    v.swap(1, 2);
    assert_eq!(v.data[1], 'a' as i32);
    assert_eq!(v.data[2], 'c' as i32);
    v.swap(1, 1);
    assert_eq!(v.data[1], 'a' as i32);
}

#[test]
fn test_vec_truncate() {
    let mut v = VecInt::new();
    for _ in 0..1000 {
        v.push(0);
    }
    v.truncate(10000);
    assert_eq!(v.len(), 1000);
    v.truncate(900);
    assert_eq!(v.len(), 900);
}

#[test]
fn test_vec_clear() {
    let mut v = VecInt::new();
    v.push(1);
    v.push(2);
    v.clear();
    assert_eq!(v.len(), 0);
}

#[test]
fn test_vec_first() {
    let mut v = VecInt::new();
    v.push(0xf00d);
    v.push(0);
    assert_eq!(v.first(), 0xf00d);
}

#[test]
fn test_vec_last() {
    let mut v = VecInt::new();
    v.push(0);
    v.push(0xf00d);
    assert_eq!(v.last(), 0xf00d);
}

#[test]
fn test_vec_reserve() {
    let mut v = VecInt::new();
    v.reserve(100);
    assert!(v.capacity() >= 100);
    v.reserve(50);
    assert!(v.capacity() >= 100);
    let mut v2 = VecInt::new();
    v2.push(123);
    v2.push(456);
    v2.reserve(200);
    assert!(v2.capacity() >= 200);
    assert_eq!(v2.reserve(300), 0);
}

#[test]
fn test_vec_compact() {
    let mut v = VecInt::new();
    for _ in 0..1000 { v.push(0); }
    v.truncate(3);
    v.compact();
    assert_eq!(v.len(), v.capacity());
    assert_eq!(v.compact(), 0);
}

#[test]
fn test_vec_pusharr() {
    let a = [5, 6, 7, 8, 9];
    let mut v = VecDouble::new();
    v.push(1.0);
    v.push(2.0);
    v.pusharr(&a, 5);
    let d = &v.data;
    assert_eq!(d[0], 1.0);
    assert_eq!(d[2], 5.0);
    assert_eq!(d[6], 9.0);
    let mut v2 = VecDouble::new();
    v2.pusharr(&a, 5);
    assert_eq!(v2.data[0], 5.0);
}

#[test]
fn test_vec_extend() {
    let mut v = VecInt::new();
    let mut v2 = VecInt::new();
    v.push(12);
    v.push(34);
    v2.push(56);
    v2.push(78);
    v.extend(&v2);
    assert_eq!(v.data[0], 12);
    assert_eq!(v.data[1], 34);
    assert_eq!(v.data[2], 56);
    assert_eq!(v.data[3], 78);
    assert_eq!(v.len(), 4);
}

#[test]
fn test_vec_find() {
    let mut v = VecInt::new();
    for i in 0..26 {
        v.push('a' as i32 + i);
    }
    assert_eq!(v.find('a' as i32), 0);
    assert_eq!(v.find('z' as i32), 25);
    assert_eq!(v.find('d' as i32), 3);
    assert_eq!(v.find('_' as i32), -1);
}

#[test]
fn test_vec_remove() {
    let mut v = VecInt::new();
    for i in 0..26 {
        v.push('a' as i32 + i);
    }
    v.remove('_' as i32);
    assert_eq!(v.len(), 26);
    v.remove('c' as i32);
    assert_eq!(v.data[0], 'a' as i32);
    assert_eq!(v.data[1], 'b' as i32);
    assert_eq!(v.data[2], 'd' as i32);
    assert_eq!(v.data[3], 'e' as i32);
    assert_eq!(v.len(), 25);
}

#[test]
fn test_vec_reverse() {
    let mut v = VecInt::new();
    v.push('a' as i32);
    v.push('b' as i32);
    v.push('c' as i32);
    v.push('d' as i32);
    v.reverse();
    assert_eq!(v.len(), 4);
    assert_eq!(v.data[0], 'd' as i32);
    assert_eq!(v.data[1], 'c' as i32);
    assert_eq!(v.data[2], 'b' as i32);
    assert_eq!(v.data[3], 'a' as i32);
}

#[test]
fn test_vec_foreach() {
    let mut v = VecInt::new();
    v.push(19); v.push(31); v.push(47);
    let mut count = 0;
    let mut acc = 1;
    for (i, &x) in v.data.iter().enumerate() {
        acc *= x + count;
        count += 1;
    }
    assert_eq!(acc, (19 + 0) * (31 + 1) * (47 + 2));
}

#[test]
fn test_vec_foreach_rev() {
    let mut v = VecInt::new();
    v.push(19); v.push(31); v.push(47);
    let mut xs = v.data.clone();
    xs.reverse();
    let mut count = 0;
    let mut acc = 1;
    for (i, &x) in xs.iter().enumerate() {
        acc *= x + count;
        count += 1;
    }
    assert_eq!(acc, (19 + 2) * (31 + 1) * (47 + 0));
}

#[test]
fn test_vec_foreach_ptr() {
    let mut v = VecInt::new();
    v.push(19); v.push(31); v.push(47);
    let mut count = 0;
    let mut acc = 1;
    for (i, x) in v.data.iter().enumerate() {
        acc *= *x + count;
        count += 1;
    }
    assert_eq!(acc, (19 + 0) * (31 + 1) * (47 + 2));
}

#[test]
fn test_vec_foreach_ptr_rev() {
    let mut v = VecInt::new();
    v.push(19); v.push(31); v.push(47);
    let mut xs = v.data.clone();
    xs.reverse();
    let mut count = 0;
    let mut acc = 1;
    for (i, x) in xs.iter().enumerate() {
        acc *= *x + count;
        count += 1;
    }
    assert_eq!(acc, (19 + 2) * (31 + 1) * (47 + 0));
}