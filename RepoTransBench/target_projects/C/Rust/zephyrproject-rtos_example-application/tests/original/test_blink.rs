use zephyrproject_rtos_example_application::{gpio_led_on, gpio_led_off};

#[test]
fn test_gpio_led_on() {
    // Normal use
    let result = gpio_led_on(1);
    assert_eq!(result, 0);
    println!("test_gpio_led_on: PASS");
}

#[test]
fn test_gpio_led_off() {
    let result = gpio_led_off(1);
    assert_eq!(result, 0);
    println!("test_gpio_led_off: PASS");
}

#[test]
fn test_gpio_led_on_negative() {
    // Edge case: negative id
    let result = gpio_led_on(-1);
    assert_eq!(result, -1);
    println!("test_gpio_led_on (negative): PASS");
}

#[test]
fn test_gpio_led_off_negative() {
    let result = gpio_led_off(-1);
    assert_eq!(result, -1);
    println!("test_gpio_led_off (negative): PASS");
}

#[test]
fn test_blink_all() {
    test_gpio_led_on();
    test_gpio_led_off();
    test_gpio_led_on_negative();
    test_gpio_led_off_negative();
    println!("test_blink: ALL PASS");
}