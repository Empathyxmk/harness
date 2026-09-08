use zephyrproject_rtos_example_application::blink_count_leds;

#[test]
fn test_blink_led_count_public() {
    // Use different values than original test_blink.rs
    let leds = blink_count_leds(2, 7);
    assert_eq!(leds, 5);

    let leds = blink_count_leds(1, 4);
    assert_eq!(leds, 3);
}

#[test]
fn test_blink_public_all() {
    println!("Running public test_blink_public.rs ...");
    test_blink_led_count_public();
    println!("test_blink_public passed!");
}