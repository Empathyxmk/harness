// Rust translation of the public C test: tests/test_hello_public.c

use agile6v_awesome_nginx::hello_main;

#[test]
fn test_hello_main_with_one_argc() {
    // Public test: different invocation, still expect 0 as return code
    let result = hello_main(1, None);
    assert_eq!(result, 0, "hello_main(1, NULL) should return 0");
}

#[test]
fn test_hello_main_with_ten_argc() {
    // Public test: call with nonzero argc and ignore argv
    let result = hello_main(10, None);
    assert_eq!(result, 0, "hello_main(10, NULL) should return 0");
}