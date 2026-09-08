use scrapy_jsonrpc::txweb::Error;

#[test]
fn test_public_error_properties() {
    let err = Error::new(1000, "unknown error", Some(serde_json::json!({"prop": "value"})));
    assert_eq!(err.code, 1000);
    assert_eq!(err.message, "unknown error");
    assert_eq!(err.data, Some(serde_json::json!({"prop": "value"})));
}

#[test]
fn test_public_error_str_repr() {
    let err = Error::new(404, "resource not here", None);
    assert_eq!(format!("{}", err), "resource not here");
    assert!(format!("{:?}", err).contains("Error(404, 'resource not here'"));
}

#[test]
fn test_public_handler_returns_not_found() {
    // Rust equivalent: test an error thrown from a handler returns correct error
    fn dummy_handler() -> Result<(), Error> {
        Err(Error::new(404, "Not Found", None))
    }
    let r = dummy_handler();
    match r {
        Err(err) => {
            assert_eq!(err.code, 404);
            assert_eq!(err.message, "Not Found");
        },
        _ => panic!("Should be error!"),
    }
}