use async2::example_entry;

#[test]
fn public_test_example_main() {
    let ret = example_entry();
    assert_eq!(ret, 42); // assuming output of private test is 42
}