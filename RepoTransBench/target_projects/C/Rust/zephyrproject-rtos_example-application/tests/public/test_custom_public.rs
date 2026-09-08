use zephyrproject_rtos_example_application::{custom_add, custom_multiply};

#[test]
fn test_custom_add_public() {
    assert_eq!(custom_add(10, 11), 21);
    assert_eq!(custom_add(-2, 5), 3);
}

#[test]
fn test_custom_multiply_public() {
    assert_eq!(custom_multiply(3, 6), 18);
    assert_eq!(custom_multiply(-3, 2), -6);
}

#[test]
fn test_custom_public_all() {
    println!("Running public test_custom_public.rs ...");
    test_custom_add_public();
    test_custom_multiply_public();
    println!("test_custom_public passed!");
}