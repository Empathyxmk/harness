// Translated from: tests/test_exceptions.py

use viralogic_py_enumerable::exceptions;

#[test]
fn test_exceptions_instantiation() {
    let e1 = exceptions::NoElementsError;
    let e2 = exceptions::NullArgumentError;
    let e3 = exceptions::NoMatchingElement;
    let e4 = exceptions::MoreThanOneMatchingElement;
    // These are errors; test that they are Error and Display
    assert!(format!("{}", e1).contains("No elements"));
    assert!(format!("{}", e2).contains("Null argument"));
    assert!(format!("{}", e3).contains("No matching element"));
    assert!(format!("{}", e4).contains("More than one matching element"));
}