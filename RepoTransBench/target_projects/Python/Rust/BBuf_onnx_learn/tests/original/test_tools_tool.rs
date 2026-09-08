use bbuf_onnx_learn::tools::tool::{add, sub, mul, div, Tool};

#[test]
fn test_basic_ops() {
    assert_eq!(add(10, 5), 15);
    assert_eq!(sub(10, 5), 5);
    assert_eq!(mul(4, 0), 0);
    assert_eq!(div(20, 4), 5);
}

#[test]
fn test_negative_values() {
    assert_eq!(sub(-5, -5), 0);
    assert_eq!(mul(-2, 3), -6);
}

#[test]
fn test_div_zero() {
    let result = std::panic::catch_unwind(|| { div(1, 0); });
    assert!(result.is_err());
}

#[test]
fn test_tool_multiply() {
    let t = Tool;
    assert_eq!(t.multiply(-1, 8), -8);
}

#[test]
fn test_tool_identity() {
    let t = Tool;
    assert_eq!(t.identity(String::from("abc")), String::from("abc"));
}