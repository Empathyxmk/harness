// Translated from: tests/test_core.py

use viralogic_py_enumerable::core::{Node, Key, OrderingDirection, RepeatableIterable};

#[test]
fn test_node_next_value() {
    // Implementing Node for test -- assuming value field is public and next (or _next) is Option<Box<Node<T>>>
    let mut n1 = Node::new(1);
    let n2 = Node::new(2);
    n1.set_next(n2.clone());
    assert_eq!(n1.value(), 1);
    assert_eq!(n1.next().unwrap().value(), 2);
}

#[test]
fn test_key_repr() {
    // Key wraps a map; let's simulate via Debug display
    let mut map = std::collections::HashMap::new();
    map.insert("a", 1);
    map.insert("b", 2);
    let k = Key::new_with_map(map.clone(), &[]);
    let r = format!("{:?}", k);
    assert!(r.contains("'a'") || r.contains("\"a\""));
    assert!(r.contains("1"));
    assert!(r.contains("'b'") || r.contains("\"b\""));
    assert!(r.contains("2"));

    let k2 = Key::new_with_args(None, &[("c", 3), ("d", 4)]);
    assert_eq!(k2.get("c"), Some(&3));
    assert_eq!(k2.get("d"), Some(&4));
}

#[test]
fn test_ordering_direction() {
    let od = OrderingDirection::new(Box::new(|x: &i32| -x), true);
    assert_eq!(od.is_descending(), true);
    assert_eq!(od.key_op(&(3)), -3);
}

#[test]
fn test_repeatable_iterable_basics() {
    let data = vec![1, 2, 3];
    let rit = RepeatableIterable::new(data.clone());
    let out: Vec<_> = rit.iter().collect();
    assert_eq!(out, data);
    assert_eq!(rit.len(), 3);
}

#[test]
fn test_repeatable_iterable_reversed() {
    let data = vec![1, 2, 3];
    let rit = RepeatableIterable::new(data.clone());
    let mut out: Vec<_> = rit.iter().rev().collect();
    out.reverse(); // Because rev+collect is reverse order for forward iterator
    assert_eq!(out, vec![3, 2, 1]);
}

#[test]
fn test_repeatable_iterable_iter_and_next() {
    let data = vec![10, 20, 30];
    let rit = RepeatableIterable::new(data.clone());
    let mut it = rit.iter();
    let result = it.next();
    assert_eq!(result, Some(&10));
    // Exhaust all
    for _ in it.by_ref() {}
    // Reset and check again: new iterator yields original data
    let vals: Vec<_> = rit.iter().collect();
    assert_eq!(vals, data);
}

#[test]
fn test_repeatable_iterable_type_error() {
    let result = std::panic::catch_unwind(|| {
        RepeatableIterable::from_not_iterable(123usize);
    });
    assert!(result.is_err());
}