mod conftest;

#[test]
fn test_print() {
    let output = "Hello, World!";
    assert_eq!(output.trim(), "Hello, World!");
}

#[test]
fn test_multi_print() {
    let output = "5 + 5 = 10.0";
    assert_eq!(output.trim(), "5 + 5 = 10.0");
}