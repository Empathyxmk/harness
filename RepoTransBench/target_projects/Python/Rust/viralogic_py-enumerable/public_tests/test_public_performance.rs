// Translated from: public_tests/test_public_performance.py

use viralogic_py_enumerable::enumerable::Enumerable;

#[test]
fn test_public_enumerable_list_performance() {
    let e = Enumerable::from((0..200).collect::<Vec<_>>());
    let l: Vec<_> = e.iter().cloned().collect();
    assert_eq!(l, (0..200).collect::<Vec<_>>());
}

#[test]
fn test_public_enumerable_tuple_performance() {
    let e = Enumerable::from((0..120).collect::<Vec<_>>());
    let l: Vec<_> = e.iter().cloned().collect();
    assert_eq!(l, (0..120).collect::<Vec<_>>());
}