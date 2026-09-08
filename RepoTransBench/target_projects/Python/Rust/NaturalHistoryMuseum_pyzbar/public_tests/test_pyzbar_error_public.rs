#[derive(Debug)]
struct PyZbarError(String);

impl std::fmt::Display for PyZbarError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}
impl std::error::Error for PyZbarError {}

#[test]
fn test_error_message() {
    let e = PyZbarError("Public test: barcode problem".to_string());
    assert_eq!(e.to_string(), "Public test: barcode problem");
}

#[test]
fn test_error_raise_and_catch() {
    let result = std::panic::catch_unwind(|| {
        panic!("{}", PyZbarError("Test error for catching".to_string()));
    });
    assert!(result.is_err());
    if let Err(e) = result {
        let msg = format!("{:?}", e);
        assert!(msg.contains("catching"));
    }
}