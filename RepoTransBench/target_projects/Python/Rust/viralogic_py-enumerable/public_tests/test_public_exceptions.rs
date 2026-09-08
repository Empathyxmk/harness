// Translated from: public_tests/test_public_exceptions.py

use viralogic_py_enumerable::exceptions::{
    EmptyCollectionException, InvalidKeyException, InvalidOperationException,
};

#[test]
fn test_empty_collection_exception_message() {
    let ex = EmptyCollectionException(String::from("Nothing to iterate with public test!"));
    assert!(format!("{}", ex).contains("Nothing to iterate"));
}

#[test]
fn test_invalid_key_exception_message() {
    let ex = InvalidKeyException(String::from("Invalid KEY provided in public test."));
    assert!(format!("{}", ex).contains("KEY provided"));
}

#[test]
fn test_invalid_operation_exception_message() {
    let ex = InvalidOperationException(String::from("Operation not allowed in public test."));
    assert!(format!("{}", ex).contains("not allowed"));
}

#[test]
fn test_empty_collection_exception_is_instance_of_exception() {
    let ex = EmptyCollectionException(String::from("Another public empty collection error."));
    assert!(format!("{}", ex).to_lowercase().contains("empty collection"));
}

#[test]
fn test_invalid_key_exception_is_instance_of_exception() {
    let ex = InvalidKeyException(String::from("Trying a different invalid key in public test."));
    assert!(format!("{}", ex).to_lowercase().contains("invalid key"));
}

#[test]
fn test_invalid_operation_exception_is_instance_of_exception() {
    let ex = InvalidOperationException(String::from("A variant operation error in public test."));
    assert!(format!("{}", ex).to_lowercase().contains("operation error"));
}