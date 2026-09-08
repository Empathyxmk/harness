use zephyrproject_rtos_example_application::{custom_add, custom_subtract};

#[test]
fn test_custom_add_function() {
    assert_eq!(custom_add(1, 2), 3);
    assert_eq!(custom_add(-1, -1), -2);
    assert_eq!(custom_add(0, 0), 0);
    println!("test_custom_add: PASS");
}

#[test]
fn test_custom_subtract_function() {
    assert_eq!(custom_subtract(3, 2), 1);
    assert_eq!(custom_subtract(-1, -1), 0);
    assert_eq!(custom_subtract(0, 1), -1);
    println!("test_custom_subtract: PASS");
}

#[test]
fn test_custom_all() {
    test_custom_add_function();
    test_custom_subtract_function();
    println!("test_custom: ALL PASS");
}