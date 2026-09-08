// Translated from: tests/test_repeatable.py

use viralogic_py_enumerable::core::RepeatableIterable;

#[test]
fn test_iter_none() {
    let ri = RepeatableIterable::new_empty();
    let sum: i32 = ri.iter().map(|_| 1).sum();
    assert_eq!(sum, 0);
}

#[test]
fn test_iter_range() {
    let ri = RepeatableIterable::from_range(0..5);
    for (i, v) in ri.iter().enumerate() {
        assert_eq!(i as i32, *v);
    }
    assert_eq!(ri.current_value(), 0);
}

#[test]
fn test_len() {
    let ri = RepeatableIterable::from_range(0..3);
    assert_eq!(ri.len(), 3);
    assert_eq!(ri.current_value(), 0);
}

#[test]
fn test_next() {
    let mut ri = RepeatableIterable::from_range(0..2);
    assert_eq!(ri.len(), 2);
    assert_eq!(ri.current_value(), 0);
    assert_eq!(ri.next(), Some(1));
    assert_eq!(ri.next(), None);
}

#[test]
fn test_iter_generator() {
    let names = vec!["Bruce", "viralogic", "software"];
    let ri = RepeatableIterable::from_iter(names.iter().cloned());
    assert_eq!(ri.len(), 3);
    let mut it = ri.iter();
    assert_eq!(it.next(), Some(&"viralogic"));
}

#[test]
fn test_reverse_chain() {
    let data: Vec<i32> = (1..4).collect();
    let mut chain = data.clone();
    chain.push(4);
    let ri = RepeatableIterable::new(chain.clone());
    let mut reversed: Vec<i32> = ri.iter().rev().cloned().collect();
    reversed.reverse(); // as in forward iter reversed
    assert_eq!(reversed, vec![4, 3, 2, 1]);
}