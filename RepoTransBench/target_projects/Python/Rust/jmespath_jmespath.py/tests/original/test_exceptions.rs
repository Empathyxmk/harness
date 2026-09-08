#[derive(Debug)]
struct ArityError {
    func: &'static str,
    expected: usize,
    received: usize,
}
impl std::fmt::Display for ArityError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "ArityError: {} expected {}, got {}", self.func, self.expected, self.received)
    }
}

#[derive(Debug)]
struct ParseError {
    position: usize,
    value: &'static str,
    token: &'static str,
    message: &'static str,
}
impl std::fmt::Display for ParseError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{} {} {}", self.position, self.token, self.message)
    }
}

#[test]
fn test_arity_error() {
    let err = ArityError{ func: "foo", expected: 1, received: 2 };
    assert!(format!("{:?}", err).contains("ArityError"));
    assert!(format!("{}", err).contains("foo"));
}

#[test]
fn test_parse_error() {
    let err = ParseError{ position: 10, value: "bad", token: "ID", message: "bad token" };
    assert!(format!("{}", err).contains("bad"));
    assert!(format!("{}", err).contains("ID"));
}

#[test]
fn test_empty_expression_error() {
    // Just check that the error struct can be instantiated.
    struct EmptyExpressionError;
    let _err = EmptyExpressionError;
}

#[test]
fn test_variadic_arity_error() {
    #[derive(Debug)]
    struct VariadictArityError(&'static str, usize, usize);
    let err = VariadictArityError("bar", 1, 2);
    assert!(format!("{:?}", err).contains("VariadictArityError"));
}

#[test]
fn test_unknown_function_error() {
    #[derive(Debug)]
    struct UnknownFunctionError(&'static str);
    let err = UnknownFunctionError("foo");
    assert!(format!("{:?}", err).contains("UnknownFunctionError"));
    assert!(format!("{:?}", err).contains("foo"));
}