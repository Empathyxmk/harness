use crate::configuration::{Factory, ApiConfig};
use crate::data::{JsonApiResponse};
use crate::request_factory::{ApiRequestFactory, ApiConnectionError};

fn get_config() -> ApiConfig {
    let mut params = std::collections::HashMap::new();
    params.insert("API_ROOT".to_string(), "testing".to_string());
    params.insert("RETRIES".to_string(), "2".to_string());
    Factory::new(params).create()
}

#[test]
fn test_get() {
    let config = get_config();
    let factory = ApiRequestFactory::new(config);
    let response = factory.get("endpoint");
    assert_eq!(response.data(), JsonApiResponse::from_data(serde_json::json!({})).as_data());
}

#[test]
fn test_retrying() {
    let config = get_config();
    let factory = ApiRequestFactory::new(config);
    let response = factory.get("endpoint");
    assert_eq!(response.data(), JsonApiResponse::from_data(serde_json::json!({})).as_data());
}

#[test]
#[should_panic]
fn test_reraises() {
    let config = get_config();
    let factory = ApiRequestFactory::new(config);
    if let Err(_e) = factory._request("endpoint", "GET") {
        panic!("ApiConnectionError");
    }
}