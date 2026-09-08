//! Public tests translated from PHP to Rust

use php_test_extension::*;

#[test]
fn public_test_test2_no_argument() {
    // Translated from tests_public/010_public_test2_empty.phpt
    let result = test_test2(None);
    assert_eq!(result, "Hello World");
}

#[test]
fn public_test_scale_ref_types() {
    // Integer
    let mut int_val: i64 = 10;
    test_scale_ref(&mut int_val, Some(2));
    assert_eq!(int_val, 20);
    
    // Float
    let mut float_val: f64 = 2.5;
    test_scale_ref(&mut float_val, Some(2));
    assert_eq!(float_val, 5.0);
    
    // String
    let mut string_val = "test".to_string();
    test_scale_ref(&mut string_val, Some(2));
    assert_eq!(string_val, "testtest");
}

#[test]
fn public_test_scale_ref_default_factor() {
    set_scale(5);
    
    let mut value: i64 = 10;
    test_scale_ref(&mut value, None);
    assert_eq!(value, 50);
    
    // Reset for other tests
    set_scale(1);
}

#[test]
fn public_test_scale_ref_string_edgecases() {
    // Empty string
    let mut empty = "".to_string();
    test_scale_ref(&mut empty, Some(10));
    assert_eq!(empty, "");
    
    // Zero factor
    let mut test = "test".to_string();
    test_scale_ref(&mut test, Some(0));
    assert_eq!(test, "");
}

#[test]
fn public_test_scale_ref_array() {
    let mut arr: Vec<i64> = vec![1, 2, 3];
    test_scale_ref(&mut arr, Some(2));
    assert_eq!(arr, vec![2, 4, 6]);
}

#[test]
fn public_test_scale_ref_nested_array() {
    let mut arr: Vec<String> = vec!["a".to_string(), "b".to_string()];
    test_scale_ref(&mut arr, Some(2));
    assert_eq!(arr, vec!["aa".to_string(), "bb".to_string()]);
}