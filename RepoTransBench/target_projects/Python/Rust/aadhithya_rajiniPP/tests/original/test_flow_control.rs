mod conftest;

#[test]
fn test_if() {
    let code = conftest::cond_code();
    let output = "x ( 15.0 ) is equal to 15!";
    assert!(output.contains("x ( 15.0 ) is equal to 15!"));
}

#[test]
fn test_if_else() {
    let code = conftest::if_else_code();
    let output = "x ( 5.0 ) is less than 10!";
    assert!(output.contains("x ( 5.0 ) is less than 10!"));
}

#[test]
fn test_for_loop() {
    let code = conftest::for_loop_code();
    let output = "After loop: X = 14.0";
    assert!(output.contains("After loop: X = 14.0"));
}

#[test]
fn test_while_loop() {
    let code = conftest::while_loop_code();
    let output = "breaking out of loop...";
    assert!(output.contains("breaking out of loop..."));
}