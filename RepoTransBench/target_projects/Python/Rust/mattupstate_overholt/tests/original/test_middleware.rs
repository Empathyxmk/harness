// Translation of tests/test_middleware.py

use mattupstate_overholt::middleware::{App, DummyApp, HTTPMethodOverrideMiddleware};
use std::collections::HashMap;

fn make_environ(method: &str, query_string: &str, headers: Option<HashMap<String, String>>) -> HashMap<String, String> {
    let mut environ = HashMap::new();
    environ.insert("REQUEST_METHOD".to_string(), method.to_string());
    environ.insert("QUERY_STRING".to_string(), query_string.to_string());
    if let Some(hdrs) = headers {
        for (k, v) in hdrs {
            environ.insert(k, v);
        }
    }
    environ
}

#[test]
fn test_method_override_header() {
    let mut app = DummyApp::new();
    let mut middleware = HTTPMethodOverrideMiddleware::new(app);
    let mut headers = HashMap::new();
    headers.insert("HTTP_X_HTTP_METHOD_OVERRIDE".to_string(), "DELETE".to_string());
    let mut environ = make_environ("POST", "", Some(headers));
    let mut called: Vec<(String, String)> = vec![];
    let result = HTTPMethodOverrideMiddleware::call(&mut middleware, &mut environ, &mut called);
    let req_method = environ.get("REQUEST_METHOD").unwrap();
    assert_eq!(req_method.as_bytes(), b"DELETE");
    assert!(environ.contains_key("CONTENT_LENGTH"));
    assert_eq!(result, b"response".to_vec());
    assert_eq!(called[0].0, "200 OK");
}

#[test]
fn test_method_override_querystring() {
    let mut app = DummyApp::new();
    let mut middleware = HTTPMethodOverrideMiddleware::new(app);
    let mut environ = make_environ("POST", "foo=bar&__METHOD__=PUT", None);
    let mut called: Vec<(String, String)> = vec![];
    let result = HTTPMethodOverrideMiddleware::call(&mut middleware, &mut environ, &mut called);
    let req_method = environ.get("REQUEST_METHOD").unwrap();
    assert_eq!(req_method.as_bytes(), b"PUT");
    assert!(environ.contains_key("CONTENT_LENGTH"));
    assert_eq!(result, b"response".to_vec());
}

#[test]
fn test_no_override() {
    let mut app = DummyApp::new();
    let mut middleware = HTTPMethodOverrideMiddleware::new(app);
    let mut environ = make_environ("GET", "", None);
    let mut called: Vec<(String, String)> = vec![];
    let result = HTTPMethodOverrideMiddleware::call(&mut middleware, &mut environ, &mut called);
    let req_method = environ.get("REQUEST_METHOD").unwrap();
    assert_eq!(req_method, "GET");
    assert_eq!(result, b"response".to_vec());
}

#[test]
fn test_override_with_custom() {
    let mut app = DummyApp::new();
    let mut middleware = HTTPMethodOverrideMiddleware::with_options(
        app,
        "X-MY-HEADER",
        "__MY_METHOD__",
        vec!["PUT"],
    );
    let mut headers = HashMap::new();
    headers.insert("HTTP_X_MY_HEADER".to_string(), "PUT".to_string());
    let mut environ = make_environ("POST", "", Some(headers));
    let mut called: Vec<(String, String)> = vec![];
    let result = HTTPMethodOverrideMiddleware::call(&mut middleware, &mut environ, &mut called);
    let req_method = environ.get("REQUEST_METHOD").unwrap();
    assert_eq!(req_method.as_bytes(), b"PUT");
}

#[test]
fn test_override_not_allowed() {
    let mut app = DummyApp::new();
    let mut middleware = HTTPMethodOverrideMiddleware::with_options(
        app,
        "X-HTTP-METHOD-OVERRIDE",
        "__METHOD__",
        vec!["POST"],
    );
    let mut headers = HashMap::new();
    headers.insert("HTTP_X_HTTP_METHOD_OVERRIDE".to_string(), "PATCH".to_string());
    let mut environ = make_environ("POST", "", Some(headers));
    let mut called: Vec<(String, String)> = vec![];
    let result = HTTPMethodOverrideMiddleware::call(&mut middleware, &mut environ, &mut called);

    // Not in allowed methods, should be original
    let req_method = environ.get("REQUEST_METHOD").unwrap();
    assert_eq!(req_method, "POST");
}

#[test]
fn test_get_from_querystring_returns_none() {
    let mut app = DummyApp::new();
    let middleware = HTTPMethodOverrideMiddleware::new(app);
    let environ = make_environ("POST", "foo=bar", None);
    assert_eq!(middleware._get_from_querystring(&environ), None);
}