// Translated from: public_tests/test_public_repeatable.py

use viralogic_py_enumerable::core::RepeatableIterable;

#[test]
fn test_public_repeatable_common_usage() {
    let items = RepeatableIterable::new(vec![10, 20, 30]);
    let vals1: Vec<_> = items.iter().cloned().collect();
    assert_eq!(vals1, vec![10, 20, 30]);
    let vals2: Vec<_> = items.iter().cloned().collect();
    assert_eq!(vals2, vec![10, 20, 30]);
    let sum: i32 = items.iter().cloned().sum();
    assert_eq!(sum, 60);

    assert!(items.iter().any(|&x| x > 25));
    assert!(items.iter().all(|&x| x < 40));
}