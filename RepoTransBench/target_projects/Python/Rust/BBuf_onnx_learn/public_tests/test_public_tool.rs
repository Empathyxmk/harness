use bbuf_onnx_learn::tools::tool;

#[test]
fn test_add() {
    assert_eq!(tool::add(5, 7), 12);
    assert_eq!(tool::add(-3, 3), 0);
    assert_eq!(tool::add(10, -10), 0);
}

#[test]
fn test_sub() {
    assert_eq!(tool::sub(10, 2), 8);
    assert_eq!(tool::sub(-10, 5), -15);
}

#[test]
fn test_mul() {
    assert_eq!(tool::mul(7, 3), 21);
    assert_eq!(tool::mul(-4, 2), -8);
}

#[test]
fn test_div() {
    assert_eq!(tool::div(8, 2), 4);
    let result = std::panic::catch_unwind(|| { tool::div(-4, 0); });
    assert!(result.is_err());
}

#[test]
fn test_tool_class() {
    let t = tool::Tool;
    assert_eq!(t.multiply(4, -2), -8);
    assert_eq!(t.identity(0), 0);
    // Can't check 'callable' in Rust; method existence is sufficient.
}