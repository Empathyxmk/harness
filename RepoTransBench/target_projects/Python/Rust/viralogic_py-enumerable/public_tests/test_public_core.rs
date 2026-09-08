// Translated from: public_tests/test_public_core.py

use viralogic_py_enumerable::core::{Node, RepeatableIterable, Key, OrderingDirection};

#[test]
fn test_public_node_next_value() {
    let mut node1 = Node::new(99);
    let node2 = Node::new(101);
    node1.set_next(node2.clone());
    assert_eq!(node1.next().unwrap().value(), 101);
}

#[test]
fn test_public_key_repr() {
    let mut map = std::collections::HashMap::new();
    map.insert("foo", 42);
    map.insert("bar", 13);
    let k = Key::new_with_map(map.clone(), &[]);
    let r = format!("{:?}", k);
    assert!(r.contains("foo") && r.contains("bar") && r.contains("42") && r.contains("13"));
}

#[test]
fn test_public_repeatable_iterable_basics() {
    let r = RepeatableIterable::new(vec![10, 11, 12]);
    let items: Vec<i32> = r.iter().cloned().collect();
    assert_eq!(items, vec![10, 11, 12]);
    assert_eq!(r.len(), 3);
}

#[test]
fn test_public_repeatable_iterable_reversed() {
    let r = RepeatableIterable::new(vec![1, 2, 3]);
    let items: Vec<i32> = r.iter().cloned().collect();
    let mut rev = items.clone();
    rev.reverse();
    assert_eq!(rev, vec![3, 2, 1]);
}

#[test]
fn test_public_repeatable_iterable_iter_and_next() {
    let r = RepeatableIterable::new(vec![41, 18]);
    let mut it = r.iter();
    assert_eq!(it.next(), Some(&41));
    assert_eq!(it.next(), Some(&18));
    assert_eq!(it.next(), None);
}

#[test]
fn test_public_repeatable_iterable_type_error() {
    let result = std::panic::catch_unwind(|| RepeatableIterable::from_not_iterable(55usize));
    assert!(result.is_err());
}