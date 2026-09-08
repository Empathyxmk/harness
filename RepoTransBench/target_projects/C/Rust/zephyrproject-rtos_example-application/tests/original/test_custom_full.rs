use zephyrproject_rtos_example_application::custom_get_value;

#[test]
fn test_custom_get_value_function() {
    let a = custom_get_value(100);
    let b = custom_get_value(0);
    println!("custom_get_value(100)={}", a);
    println!("custom_get_value(0)={}", b);
    assert_eq!(a, 100, "FAIL: expected 100");
    assert_eq!(b, 42, "FAIL: expected default (42)");
}

#[test]
fn test_custom_full_pass() {
    test_custom_get_value_function();
    println!("test_custom_full PASS");
}