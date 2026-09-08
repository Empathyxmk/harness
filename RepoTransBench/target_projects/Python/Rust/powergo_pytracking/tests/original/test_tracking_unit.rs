use powergo_pytracking_rs::pytracking::tracking::{Configuration, TRACKING_PIXEL, PNG_MIME_TYPE, DEFAULT_TIMEOUT_SECONDS};
use base64;
use serde_json::{json, Value};
use std::collections::HashMap;

const DUMMY_URL: &str = "http://example.com";
const DUMMY_WEBHOOK: &str = "http://webhook.com";

fn dummy_key() -> Vec<u8> {
    base64::encode_config([0u8; 32], base64::URL_SAFE).into_bytes()
}

#[test]
fn test_configuration_basic_init_fields() {
    let mut default_metadata = HashMap::new();
    default_metadata.insert("x".to_string(), json!(1));
    let config = Configuration::from_args(
        Some(DUMMY_WEBHOOK),
        Some(10),
        Some(true),
        Some("http://open.example.com"),
        Some("http://click.example.com"),
        Some(default_metadata.clone()),
        Some(true),
        None,
        Some("utf-8"),
        Some(true),
    );
    assert_eq!(config.webhook_url.as_ref().unwrap(), DUMMY_WEBHOOK);
    assert_eq!(config.webhook_timeout_seconds, Some(10));
    assert_eq!(config.base_open_tracking_url.as_ref().unwrap(), "http://open.example.com");
    assert!(config.include_webhook_url.unwrap());
    assert!(config.include_default_metadata.unwrap());
    assert_eq!(config.append_slash.unwrap(), false);
}

#[test]
fn test_str_and_deepcopy_and_merge() {
    let config_1 = Configuration::from_args(
        Some("A"),
        None,
        None,
        Some("B"),
        Some("C"),
        None,
        None,
        None,
        None,
        None,
    );
    let s = format!("{}", config_1);
    assert!(s.contains("<pytracking.Configuration>"));
    let cp = config_1.__deepcopy__(());
    assert_eq!(cp.webhook_url, config_1.webhook_url);
    let mut args = HashMap::new();
    args.insert("webhook_url".to_string(), json!("D"));
    let new_c = config_1.merge_with_kwargs(args);
    assert_eq!(new_c.webhook_url, Some("D".to_string()));
    assert_eq!(new_c.base_open_tracking_url, Some("B".to_string()));
}

#[test]
fn test_get_data_to_embed_base_and_metadata() {
    let mut default_metadata = HashMap::new();
    default_metadata.insert("foo".to_string(), json!("bar"));
    let config = Configuration::from_args(
        Some(DUMMY_WEBHOOK),
        None,
        Some(true),
        Some("ooo"),
        Some("ccc"),
        Some(default_metadata.clone()),
        Some(true),
        None,
        None,
        None,
    );
    let mut user_metadata = HashMap::new();
    user_metadata.insert("meta".to_string(), json!(1));
    let data = config.get_data_to_embed(Some(DUMMY_URL), Some(user_metadata.clone()));
    assert_eq!(data.get("url").unwrap(), DUMMY_URL);
    assert!(data.contains_key("metadata"));
    let metadata = data.get("metadata").unwrap().as_object().unwrap();
    assert_eq!(metadata.get("foo").unwrap(), "bar");
    assert_eq!(metadata.get("meta").unwrap(), &json!(1));
    assert_eq!(data.get("webhook").unwrap(), DUMMY_WEBHOOK);

    let config_2 = Configuration::default();
    let res = config_2.get_data_to_embed(None, None);
    assert!(res.is_empty());

    let res_2 = config_2.get_data_to_embed(Some("http://x"), None);
    assert_eq!(res_2.get("url").unwrap(), "http://x");
}

#[test]
fn test_get_url_encoded_data_str_without_encryption() {
    let cfg = Configuration::from_args(
        None, None, None, None, None, None, None, None, Some("utf-8"), None,
    );
    let mut plain = HashMap::new();
    plain.insert("key".to_string(), json!("value"));
    let b64str = cfg.get_url_encoded_data_str(&plain);
    let decoded_bytes = base64::decode_config(&b64str, base64::URL_SAFE).unwrap();
    let decoded: Value = serde_json::from_slice(&decoded_bytes).unwrap();
    assert_eq!(decoded, json!({"key":"value"}));
}

#[test]
fn test_repr_and_defaults() {
    let config = Configuration::default();
    assert_eq!(PNG_MIME_TYPE, "image/png");
    assert!(TRACKING_PIXEL.len() > 0);
    assert_eq!(config.encryption_key, None);
    assert_eq!(config.webhook_timeout_seconds, Some(DEFAULT_TIMEOUT_SECONDS));
}

#[test]
fn test_merge_with_kwargs_does_not_change_original() {
    let cfg = Configuration::from_args(
        Some("x"),
        None, None, None, None, None, None, None, None, None,
    );
    let mut args = HashMap::new();
    args.insert("webhook_url".to_string(), json!("y"));
    let newcfg = cfg.merge_with_kwargs(args);
    assert_eq!(newcfg.webhook_url, Some("y".to_string()));
    assert_eq!(cfg.webhook_url, Some("x".to_string()));
}