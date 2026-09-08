use std::fmt;

#[derive(Debug)]
struct PyZbarError {
    msg: String,
}

impl fmt::Display for PyZbarError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.msg)
    }
}
impl std::error::Error for PyZbarError {}

impl PyZbarError {
    fn new<S: Into<String>>(msg: S) -> Self {
        Self { msg: msg.into() }
    }
}

#[test]
fn test_pyzbar_error_is_exception() {
    // In Rust, all custom errors are usually subtypes of std::error::Error
    let e = PyZbarError::new("test");
    let _ = &e as &dyn std::error::Error;
}

#[test]
fn test_pyzbar_error_raise_and_str() {
    let e = PyZbarError::new("fail");
    // Simulate raising and catching the error
    let result = std::panic::catch_unwind(|| {
        panic!("{}", e);
    });
    assert!(result.is_err());
    assert_eq!(format!("{}", e), "fail");
}