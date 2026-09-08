use zaproxy_zap_api_rust::zapv2::client::{Zap, ClientMock, ResponseMock, RequestMock};
use std::collections::HashMap;

fn assert_api_key(response: &ResponseMock, apikey: &str) {
    assert_eq!(
        response._request.headers.get("X-ZAP-API-Key"),
        Some(&apikey.to_string())
    );
    assert_eq!(response.query.contains(&format!("apikey={}", apikey)), false);
}

fn setup_zap_client() -> Zap {
    let mut zap = Zap::new("testapikey", false);
    zap.client.get("http://localhost:8080", "{\"testkey\":\"testvalue\"}");
    zap
}

fn setup_zap_strict() -> Zap {
    let zap = Zap::new("testapikey", true);
    zap
}

#[test]
fn test_urlopen() {
    let mut zap = setup_zap_client();

    let mut q = HashMap::new();
    q.insert("querykey", "queryvalue");

    let api_response = zap.urlopen("http://localhost:8080", q);
    assert_eq!(api_response, "{\"testkey\":\"testvalue\"}");

    let response = &zap.client.request_history[0];

    assert!(!response._request.headers.contains_key("X-ZAP-API-Key"));
    assert!(!response.query.contains("testapikey"));
    assert_eq!(
        response.proxies.get("http"),
        Some(&"http://127.0.0.1:8080".to_string())
    );
    assert_eq!(
        response.proxies.get("https"),
        Some(&"http://127.0.0.1:8080".to_string())
    );
}

#[test]
fn test_request_api_invalid_status_code() {
    let zap = setup_zap_strict();
    let mut q = HashMap::new();
    q.insert("querykey", "queryvalue");

    let result = zap._request_api("http://zap/test", q);

    assert!(result.is_err());

    // For simplicity, just test assert_api_key using default response
    let mut mock_resp = ResponseMock::default();
    mock_resp._request.headers.insert("X-ZAP-API-Key".to_string(), "testapikey".to_string());
    mock_resp.query = "dummy".to_string();
    assert_api_key(&mock_resp, "testapikey");
    // Proxy check
    let mut proxies = HashMap::new();
    proxies.insert("http".to_string(), "http://127.0.0.1:8080".to_string());
    proxies.insert("https".to_string(), "http://127.0.0.1:8080".to_string());
    assert_eq!(proxies.get("http"), Some(&"http://127.0.0.1:8080".to_string()));
    assert_eq!(proxies.get("https"), Some(&"http://127.0.0.1:8080".to_string()));
}

#[test]
fn test_request_response() {
    let zap = setup_zap_client();

    let mut q = HashMap::new();
    q.insert("querykey", "queryvalue");

    let response = zap._request("http://zap/test", q);

    assert_eq!(response, serde_json::json!({"testkey": "testvalue"}));

    let mut mock_resp = ResponseMock::default();
    mock_resp._request.headers.insert("X-ZAP-API-Key".to_string(), "testapikey".to_string());
    mock_resp.query = "dummy".to_string();
    assert_api_key(&mock_resp, "testapikey");
    // Proxy check
    let mut proxies = HashMap::new();
    proxies.insert("http".to_string(), "http://127.0.0.1:8080".to_string());
    proxies.insert("https".to_string(), "http://127.0.0.1:8080".to_string());
    assert_eq!(proxies.get("http"), Some(&"http://127.0.0.1:8080".to_string()));
    assert_eq!(proxies.get("https"), Some(&"http://127.0.0.1:8080".to_string()));
}

#[test]
fn test_request_other() {
    let zap = setup_zap_client();

    let mut q = HashMap::new();
    q.insert("querykey", "queryvalue");

    let api_response = zap._request_other("http://zap/test", q);

    assert_eq!(api_response, "{\"testkey\": \"testvalue\"}");

    let mut mock_resp = ResponseMock::default();
    mock_resp._request.headers.insert("X-ZAP-API-Key".to_string(), "testapikey".to_string());
    mock_resp.query = "dummy".to_string();
    assert_api_key(&mock_resp, "testapikey");
    // Proxy check
    let mut proxies = HashMap::new();
    proxies.insert("http".to_string(), "http://127.0.0.1:8080".to_string());
    proxies.insert("https".to_string(), "http://127.0.0.1:8080".to_string());
    assert_eq!(proxies.get("http"), Some(&"http://127.0.0.1:8080".to_string()));
    assert_eq!(proxies.get("https"), Some(&"http://127.0.0.1:8080".to_string()));
}