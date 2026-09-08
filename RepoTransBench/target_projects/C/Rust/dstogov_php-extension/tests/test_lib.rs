//! Original tests translated from PHP to Rust

use php_test_extension::*;

#[test]
fn test_test1_works() {
    let result = test_test1();
    assert!(result.contains("test is loaded and working"));
}

#[test]
fn test_test2_default() {
    let result = test_test2(None);
    assert_eq!(result, "Hello World");
}

#[test]
fn test_test2_with_parameter() {
    let result = test_test2(Some("Rust"));
    assert_eq!(result, "Hello Rust");
}

#[test]
fn test_test2_empty_string() {
    // Translated from tests/011_test2_empty.phpt
    let result = test_test2(Some(""));
    assert_eq!(result, "Hello ");
}

#[test]
fn test_scale_ref_long() {
    let mut value: i64 = 5;
    test_scale_ref(&mut value, Some(2));
    assert_eq!(value, 10);
}

#[test]
fn test_scale_ref_double() {
    let mut value: f64 = 5.5;
    test_scale_ref(&mut value, Some(2));
    assert_eq!(value, 11.0);
}

#[test]
fn test_scale_ref_string() {
    let mut value = "abc".to_string();
    test_scale_ref(&mut value, Some(2));
    assert_eq!(value, "abcabc");
}

#[test]
fn test_scale_ref_array() {
    let mut value: Vec<i64> = vec![1, 2, 3];
    test_scale_ref(&mut value, Some(2));
    assert_eq!(value, vec![2, 4, 6]);
}

#[test]
fn test_scale_ref_nested_array() {
    let mut value: Vec<String> = vec!["a".to_string(), "b".to_string()];
    test_scale_ref(&mut value, Some(3));
    assert_eq!(value, vec!["aaa".to_string(), "bbb".to_string()]);
}

#[test]
fn test_scale_ref_default_factor() {
    // First, ensure the default scale is 1
    set_scale(1);
    
    let mut value: i64 = 5;
    test_scale_ref(&mut value, None);
    assert_eq!(value, 5);
    
    // Now change the default scale and test again
    set_scale(3);
    let mut value: i64 = 5;
    test_scale_ref(&mut value, None);
    assert_eq!(value, 15);
    
    // Reset the scale for other tests
    set_scale(1);
}

#[test]
fn test_scale_ref_string_edgecases() {
    // Test with empty string
    let mut value = "".to_string();
    test_scale_ref(&mut value, Some(3));
    assert_eq!(value, "");
    
    // Test with factor 0 (should clear the string)
    let mut value = "test".to_string();
    test_scale_ref(&mut value, Some(0));
    assert_eq!(value, "");
    
    // Test with large factor
    let mut value = "a".to_string();
    test_scale_ref(&mut value, Some(5));
    assert_eq!(value, "aaaaa");
}