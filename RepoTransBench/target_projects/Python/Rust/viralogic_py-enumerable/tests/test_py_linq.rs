// Translated from: tests/test_py_linq.py

use viralogic_py_enumerable::enumerable::Enumerable;
use viralogic_py_enumerable::exceptions::NoElementsError;

#[test]
fn test_enumerable_to_list() {
    let e = Enumerable::from(vec![1, 2, 3]);
    assert_eq!(e.to_list(), vec![1, 2, 3]);
}

#[test]
fn test_enumerable_repr_and_getitem() {
    let e = Enumerable::from(vec![10, 11, 12]);
    let r = format!("{:?}", e);
    assert!(r.contains("10") && r.contains("12"));
    assert_eq!(e.get(1), Some(11));
}

#[test]
fn test_enumerable_len_iter_reversed() {
    let e = Enumerable::from(vec![1, 2, 3, 4]);
    assert_eq!(e.len(), 4);
    let orig: Vec<_> = e.iter().cloned().collect();
    assert_eq!(orig, vec![1, 2, 3, 4]);
    let rev: Vec<_> = e.iter().rev().cloned().collect();
    assert_eq!(rev, vec![4, 3, 2, 1]);
}

#[test]
fn test_enumerable_count_predicate() {
    let e = Enumerable::from(vec![1, 2, 3, 4]);
    assert_eq!(e.count_where(|&x| x > 2), 2);
    assert_eq!(e.len(), 4);
}

#[test]
fn test_enumerable_select_sum_min_max_avg() {
    let e = Enumerable::from(vec![1, 2, 3]);
    let selected = e.select(|x| x * 2);
    assert_eq!(selected.to_list(), vec![2, 4, 6]);
    assert_eq!(e.sum(None), 6);
    assert_eq!(e.sum(Some(|x| x + 1)), 9);
    assert_eq!(e.min(None), Some(1));
    assert_eq!(e.max(None), Some(3));
    assert!((e.avg(None).unwrap() - 2.0).abs() < 1e-9);
    assert!((e.avg(Some(|x| x + 1)).unwrap() - 3.0).abs() < 1e-9);
}

#[test]
fn test_enumerable_min_max_avg_empty() {
    let e = Enumerable::<i32>::from(vec![]);
    assert!(e.min(None).is_none());
    assert!(e.max(None).is_none());
    assert!(e.avg(None).is_none());
}