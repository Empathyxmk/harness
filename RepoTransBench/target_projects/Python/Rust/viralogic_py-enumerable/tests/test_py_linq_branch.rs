// Translated from: tests/test_py_linq_branch.py

use viralogic_py_enumerable::enumerable::Enumerable;
use viralogic_py_enumerable::exceptions::{NoElementsError, NullArgumentError};

#[test]
fn test_getitem_out_of_range() {
    let e = Enumerable::from(vec![1, 2, 3]);
    assert_eq!(e.get(10), None);
}

#[test]
fn test_count_predicate_none_vs_func() {
    let data = vec![4, 5, 6];
    let e = Enumerable::from(data.clone());
    let cnt_pred = e.count_where(|&x| x > 4);
    let cnt = e.len();
    assert_eq!(cnt_pred, 2);
    assert_eq!(cnt, data.len());
}

#[test]
fn test_repr_non_ascii() {
    let obj = vec![("á", 1), ("β", 2)];
    let e = Enumerable::from(obj.clone());
    let r = format!("{:?}", e);
    assert!(r.contains("á") && r.contains("β"));
}

#[test]
fn test_select_identity_vs_func() {
    let e1 = Enumerable::from(vec![4, 5]);
    assert_eq!(e1.select(|x| *x).to_list(), vec![4, 5]);
    let e2 = Enumerable::from(vec![4, 5]);
    let l: Vec<_> = e2.select(|x| x + 3).to_list();
    assert_eq!(l, vec![7, 8]);
}

#[test]
fn test_sum_with_func() {
    let data = vec![1, 2, 3];
    let e = Enumerable::from(data.clone());
    let total = e.sum(Some(|x| x * 3));
    assert_eq!(total, 18);
}

#[test]
fn test_min_max_with_func() {
    let data = vec![3, 2, 5];
    let e = Enumerable::from(data.clone());
    let result_min = e.min(Some(|x| -x));
    let result_max = e.max(Some(|x| -x));
    assert_eq!(result_min, Some(-5));
    assert_eq!(result_max, Some(-2));
}

#[test]
fn test_next_dunder_next() {
    let e = Enumerable::from(vec![10, 20]);
    let mut it = e.iter();
    assert_eq!(it.next(), Some(&10));
    assert_eq!(it.next(), Some(&20));
    assert_eq!(it.next(), None);
}

#[test]
fn test_enumerable_empty_avg() {
    let e = Enumerable::<i32>::from(vec![]);
    assert!(e.avg(Some(|x| x * x)).is_none());
}