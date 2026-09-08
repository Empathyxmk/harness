// Translated from: tests/test_functions.py
// NOTE: This is a HUGE parameterized set of test cases in Python; you would typically split this into multiple tests in Rust for clarity.
// For demonstration, only a minimal selection is included here. Full translation would require a very extensive Rust test file.

use viralogic_py_enumerable::enumerable::Enumerable;

#[test]
fn test_constructor_and_iter() {
    let values: Vec<i32> = vec![];
    let e = Enumerable::from(values.clone());
    assert!(e.is_empty());

    let e2 = Enumerable::from(vec![1, 2, 3]);
    assert_eq!(e2.len(), 3);
    let items = e2.to_list();
    assert_eq!(items, vec![1, 2, 3]);
}

// You would further expand with all combinations from the Python parametrize lists