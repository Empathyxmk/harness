use zephyrproject_rtos_example_application::custom_sum_array;

#[test]
fn test_custom_full_sum_array_public() {
    let arr1 = [3, 6, 9];
    let arr2 = [-2, 4, 10, 0];
    assert_eq!(custom_sum_array(&arr1), 18);
    assert_eq!(custom_sum_array(&arr2), 12);
}

#[test]
fn test_custom_full_public_all() {
    println!("Running public test_custom_full_public.rs ...");
    test_custom_full_sum_array_public();
    println!("test_custom_full_public passed!");
}