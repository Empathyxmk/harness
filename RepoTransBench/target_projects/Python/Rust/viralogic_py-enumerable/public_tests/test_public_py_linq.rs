// Translated from: public_tests/test_public_py_linq.py

use viralogic_py_enumerable::enumerable::Enumerable;
use viralogic_py_enumerable::exceptions::NoElementsError;

#[test]
fn test_public_enumerable_to_list() {
    let e = Enumerable::from((13..16).collect::<Vec<_>>());
    assert_eq!(e.to_list(), vec![13, 14, 15]);
}

#[test]
fn test_public_enumerable_repr_and_getitem() {
    let vals = vec!["foo", "bar", "baz"];
    let e = Enumerable::from(vals.clone());
    let r = format!("{:?}", e);
    assert!(r.contains("foo") && r.contains("baz"));
    assert_eq!(e.get(0), Some("foo"));
    assert_eq!(e.get(2), Some("baz"));
}

#[test]
fn test_public_enumerable_len_iter_reversed() {
    let e = Enumerable::from(vec![7, 8, 9, 10]);
    assert_eq!(e.len(), 4);
    let iter_items: Vec<_> = e.iter().cloned().collect();
    assert_eq!(iter_items, vec![7, 8, 9, 10]);
    let mut reversed = iter_items.clone();
    reversed.reverse();
    assert_eq!(reversed, vec![10, 9, 8, 7]);
}

#[test]
fn test_public_enumerable_count_predicate() {
    let e = Enumerable::from(vec![1, 10, 100, 1000]);
    let cnt = e.count_where(|&x| x > 9);
    assert_eq!(cnt, 3);
}

#[test]
fn test_public_enumerable_select_sum_min_max_avg() {
    let e = Enumerable::from(vec![22, 4, 7]);
    let s = e.select(|x| x + 1).sum(None);
    assert_eq!(s, 23 + 5 + 8);

    let m = e.min(None).unwrap();
    let M = e.max(None).unwrap();
    assert_eq!((m, M), (4, 22));

    let avg = e.avg(None).unwrap();
    assert!((avg - (22.0 + 4.0 + 7.0) / 3.0).abs() < 1e-9);
}

#[test]
fn test_public_enumerable_min_max_avg_empty() {
    let ee = Enumerable::<i32>::from(vec![]);
    assert!(ee.min(None).is_none());
    assert!(ee.max(None).is_none());
    assert!(ee.avg(None).is_none());
}