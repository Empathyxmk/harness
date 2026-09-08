use zephyrproject_rtos_example_application::example_sensor_read;

#[test]
fn test_example_sensor_read_function() {
    let val = example_sensor_read();
    assert_eq!(val, 42);
    println!("test_example_sensor_read: PASS");
}

#[test]
fn test_example_sensor_all() {
    test_example_sensor_read_function();
    println!("test_example_sensor: ALL PASS");
}