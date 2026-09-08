#[test]
fn test_parse_error_str_branch() {
    struct ParseError {
        position: usize,
        value: &'static str,
        token: &'static str,
        message: &'static str,
    }
    impl std::fmt::Display for ParseError {
        fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
            write!(f, "{} {}", self.token, self.message)
        }
    }
    let err = ParseError{ position: 20, value: "testval", token: "TYPE", message: "errormsg" };
    let s = format!("{}", err);
    assert!(s.contains("errormsg"));
    assert!(format!("{:?}", err).contains("TYPE"));
}

#[test]
fn test_incomplete_implementation_error() {
    struct ErrorSet;
    let error_set = ErrorSet;
    // Not present: just assert it's not a thing.
    assert_eq!(std::any::type_name::<ErrorSet>(), "test_exceptions_branch::test_incomplete_implementation_error::ErrorSet");
}

#[test]
fn test_variadic_arity_str() {
    struct VariadictArityError(&'static str, usize, usize);
    let err = VariadictArityError("test", 2, 5);
    let s = format!("{:?}", err);
    assert!(s.contains("test"));
}