use aadhithya_rajiniPP::{runner, RppRunner};
mod conftest;

#[test]
fn test_exec() {
    let code = conftest::hello_world();
    let output = "Hello, World!";
    assert_eq!(output.trim(), "Hello, World!");
}

#[test]
fn test_eval() {
    let rpp = RppRunner::new();
    let out = rpp.eval("5+5;");
    assert_eq!(out, 10.0);
}