use bbuf_onnx_learn::tools::tool::{add, sub, mul, div, Tool};

#[test]
fn test_add() {
    assert_eq!(add(1, 2), 3);
    assert_eq!(add(-2, 2), 0);
    assert_eq!(add(0, 0), 0);
}

#[test]
fn test_sub() {
    assert_eq!(sub(3, 2), 1);
    assert_eq!(sub(-1, 1), -2);
}

#[test]
fn test_mul() {
    assert_eq!(mul(3, 2), 6);
    assert_eq!(mul(0, 8), 0);
}

#[test]
fn test_div() {
    assert_eq!(div(6, 3), 2);
    let result = std::panic::catch_unwind(|| { div(3, 0); });
    assert!(result.is_err());
}

#[test]
fn test_tool_class() {
    let t = Tool;
    assert_eq!(t.multiply(2, 3), 6);
    assert_eq!(t.identity(10), 10);
    // Rust: all methods on Tool are callable, but identity is a method.
    // We can't test 'callable', but usage in Rust always is callable if accessible.
}