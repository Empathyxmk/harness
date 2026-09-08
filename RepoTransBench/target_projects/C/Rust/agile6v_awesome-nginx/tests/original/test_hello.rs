// Rust translation of the original C test: test_hello.c

use agile6v_awesome_nginx::hello_main;

#[test]
fn test_hello_main_with_zero_argc() {
    // Test that hello_main returns 0 (success status)
    let result = hello_main(0, None);
    assert_eq!(result, 0, "hello_main(0, NULL) should return 0");
}

#[test]
fn test_hello_main_with_two_argc() {
    // Test that hello_main returns 0 for argc=2 (ignored in implementation)
    let result = hello_main(2, None);
    assert_eq!(result, 0, "hello_main(2, NULL) should return 0");
}