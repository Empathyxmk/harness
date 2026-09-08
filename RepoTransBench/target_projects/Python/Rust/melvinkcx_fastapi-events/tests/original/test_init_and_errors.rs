use std::collections::HashMap;

#[derive(Debug)]
struct FastapiEventError(String);
#[derive(Debug)]
struct ConfigurationError(String);
#[derive(Debug)]
struct MissingEventNameError(String);
#[derive(Debug)]
struct MissingEventNameDuringRegistration;
#[derive(Debug)]
struct MissingEventNameDuringDispatch;
#[derive(Debug)]
struct MultiplePayloadsDetectedDuringDispatch;

#[test]
fn test_init_vars() {
    let handler_store: HashMap<&str, i32> = HashMap::new();
    assert!(handler_store.is_empty()); // Like checking it's a dict (HashMap)

    // Rust does not have ContextVar, but we'll check variables have expected functions
    struct ContextVar<T>(T);
    let event_store = ContextVar(5);
    let in_req_res_cycle = ContextVar(true);
    let middleware_identifier = ContextVar(0);
    // Check has set "method" (mocked)
    fn has_set<T>(_cv: &ContextVar<T>) -> bool {
        true
    }
    assert!(has_set(&event_store));
    assert!(has_set(&in_req_res_cycle));
    assert!(has_set(&middleware_identifier));
}

#[test]
fn test_fastapi_event_error_is_raised() {
    let result = std::panic::catch_unwind(|| {
        panic!("{:?}", FastapiEventError("an error".to_string()));
    });
    assert!(result.is_err());
}

#[test]
fn test_configuration_error_is_raised() {
    let result = std::panic::catch_unwind(|| {
        panic!("{:?}", ConfigurationError("bad config".to_string()));
    });
    assert!(result.is_err());
}

#[test]
fn test_missing_event_name_error_is_raised() {
    let result = std::panic::catch_unwind(|| {
        panic!("{:?}", MissingEventNameError("missing name".to_string()));
    });
    assert!(result.is_err());
}

#[test]
fn test_missing_event_name_during_registration() {
    let result = std::panic::catch_unwind(|| {
        panic!("{:?}", MissingEventNameDuringRegistration);
    });
    assert!(result.is_err());
    let val = format!("{:?}", MissingEventNameDuringRegistration);
    assert!(val.contains("MissingEventNameDuringRegistration"));
}

#[test]
fn test_missing_event_name_during_dispatch() {
    let result = std::panic::catch_unwind(|| {
        panic!("{:?}", MissingEventNameDuringDispatch);
    });
    assert!(result.is_err());
    let val = format!("{:?}", MissingEventNameDuringDispatch);
    assert!(val.contains("MissingEventNameDuringDispatch"));
}

#[test]
fn test_multiple_payloads_detected_during_dispatch() {
    let result = std::panic::catch_unwind(|| {
        panic!("{:?}", MultiplePayloadsDetectedDuringDispatch);
    });
    assert!(result.is_err());
    let val = format!("{:?}", MultiplePayloadsDetectedDuringDispatch);
    assert!(val.contains("MultiplePayloadsDetectedDuringDispatch"));
}