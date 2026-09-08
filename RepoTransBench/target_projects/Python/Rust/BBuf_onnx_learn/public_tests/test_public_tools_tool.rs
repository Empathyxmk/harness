use bbuf_onnx_learn::tools::tool::{add, sub, mul, div, Tool};

#[test]
fn test_basic_ops() {
    assert_eq!(add(20, 15), 35);
    assert_eq!(sub(30, 25), 5);
    assert_eq!(mul(6, 1), 6);
    assert_eq!(div(81, 9), 9);
}

#[test]
fn test_negative_values() {
    assert_eq!(sub(-10, 5), -15);
    assert_eq!(mul(5, -5), -25);
}

#[test]
fn test_div_zero() {
    let result = std::panic::catch_unwind(|| { div(-10, 0); });
    assert!(result.is_err());
}

#[test]
fn test_tool_multiply() {
    let t = Tool;
    assert_eq!(t.multiply(9, 0), 0);
}

#[test]
fn test_tool_identity() {
    let t = Tool;
    assert_eq!(t.identity(vec![1, String::from("x"), 3]), vec![1, String::from("x"), 3]);
}