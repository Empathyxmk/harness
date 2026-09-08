use zephyrproject_rtos_example_application::fake_sensor_read;

#[test]
fn test_example_sensor_read_public() {
    assert_eq!(fake_sensor_read(5), 200);
    assert_eq!(fake_sensor_read(2), 123);
    assert_eq!(fake_sensor_read(-1), -1);
}

#[test]
fn test_example_sensor_public_all() {
    println!("Running public test_example_sensor_public.rs ...");
    test_example_sensor_read_public();
    println!("test_example_sensor_public passed!");
}