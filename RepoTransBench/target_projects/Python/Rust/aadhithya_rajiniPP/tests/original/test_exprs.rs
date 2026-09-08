mod conftest;

#[test]
fn test_conditional_exprs() {
    let code = conftest::cond_code();
    let output = "x ( 15.0 ) is equal to 15!";
    assert!(output.contains("x ( 15.0 ) is equal to 15!"));
}

#[test]
fn test_logical_exprs() {
    let code = conftest::logic_code();
    let output = "x != b:  True";
    assert!(output.contains("x != b:  True"));
}

#[test]
fn test_math_exprs() {
    let code = conftest::math_code();
    let output = "modvar =  1.0";
    assert!(output.contains("modvar =  1.0"));
}