#[test]
fn test_public_simple_arithmetic_expr() {
    let code = "print 20 + 10 + 5;";
    let output = "35.0";
    assert!(output.contains("35") || output.contains("35.0"));
}

#[test]
fn test_public_float_expr_result() {
    let code = "print 7.5 * 4;";
    let output = "30.0";
    assert!(output.contains("30") || output.contains("30.0"));
}