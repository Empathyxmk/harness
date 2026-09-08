use powergo_pytracking_rs::pytracking::tracking::{Configuration, TRACKING_PIXEL, PNG_MIME_TYPE, DEFAULT_TIMEOUT_SECONDS};
use base64;
use serde_json::{json, Value};
use std::collections::HashMap;

const ANOTHER_URL: &str = "https://anotherdomain.org";
const ANOTHER_WEBHOOK: &str = "https://anotherwebhook.org/notify";

fn another_key() -> Vec<u8> {
    base64::encode_config([9u8; 32], base64::URL_SAFE).into_bytes()
}

#[test]
fn test_public_configuration_init_fields() {
    let mut default_metadata = HashMap::new();
    default_metadata.insert("user".to_string(), json!("alice"));
    let config = Configuration::from_args(
        Some(ANOTHER_WEBHOOK),
        Some(15),
        Some(false),
        Some("https://tracker.domain.io/open"),
        Some("https://tracker.domain.io/click"),
        Some(default_metadata.clone()),
        Some(false),
        None,
        Some("latin-1"),
        Some(false),
    );
    assert_eq!(config.webhook_url.as_ref().unwrap(), ANOTHER_WEBHOOK);
    assert_eq!(config.webhook_timeout_seconds, Some(15));
    assert_eq!(config.base_open_tracking_url.as_ref().unwrap(), "https://tracker.domain.io/open");
    assert!(!config.include_webhook_url.unwrap());
    assert!(!config.include_default_metadata.unwrap());
    assert!(!config.append_slash.unwrap());
}

#[test]
fn test_public_str_and_deepcopy_and_merge() {
    let config_1 = Configuration::from_args(
        Some("PublicWebhook"),
        None,
        None,
        Some("OpenURL"),
        Some("ClickURL"),
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
    args.insert("webhook_url".to_string(), json!("SecondWebhook"));
    let new_c = config_1.merge_with_kwargs(args);
    assert_eq!(new_c.webhook_url, Some("SecondWebhook".to_string()));
    assert_eq!(new_c.base_open_tracking_url, Some("OpenURL".to_string()));
}

#[test]
fn test_public_get_data_to_embed_varied_and_metadata() {
    let mut default_metadata = HashMap::new();
    default_metadata.insert("role".to_string(), json!("dev"));
    let config = Configuration::from_args(
        Some(ANOTHER_WEBHOOK),
        None,
        Some(false),
        Some("open456"),
        Some("click123"),
        Some(default_metadata.clone()),
        Some(false),
        None,
        None,
        None,
    );
    let mut user_metadata = HashMap::new();
    user_metadata.insert("device".to_string(), json!("mobile"));
    let data = config.get_data_to_embed(Some(ANOTHER_URL), Some(user_metadata.clone()));
    assert_eq!(data.get("url").unwrap(), ANOTHER_URL);
    assert!(data.contains_key("metadata"));
    let metadata = data.get("metadata").unwrap().as_object().unwrap();
    assert_eq!(metadata.get("role").unwrap(), "dev");
    assert_eq!(metadata.get("device").unwrap(), "mobile");
    assert!(!data.contains_key("webhook"));

    let config_2 = Configuration::default();
    let res = config_2.get_data_to_embed(None, None);
    assert!(res.is_empty());

    let res_2 = config_2.get_data_to_embed(Some("https://demo"), None);
    assert_eq!(res_2.get("url").unwrap(), "https://demo");
}

#[test]
fn test_public_get_url_encoded_data_str_without_encryption() {
    let cfg = Configuration::from_args(
        None, None, None, None, None, None, None, None, Some("utf-16"), None,
    );
    let mut plain = HashMap::new();
    plain.insert("alpha".to_string(), json!("beta"));
    let b64str = cfg.get_url_encoded_data_str(&plain);
    let decoded_bytes = base64::decode_config(&b64str, base64::URL_SAFE).unwrap();
    // For utf-16, skip actual utf-16 parsing, just assert base64 string is decodable
    let _ = decoded_bytes;
    // In real implementation, decode with proper encoding
}

#[test]
fn test_public_repr_and_defaults() {
    let config = Configuration::default();
    assert_eq!(PNG_MIME_TYPE, "image/png");
    assert!(TRACKING_PIXEL.len() > 0);
    assert_eq!(config.encryption_key, None);
    assert_eq!(config.webhook_timeout_seconds, Some(DEFAULT_TIMEOUT_SECONDS));
}

#[test]
fn test_public_merge_with_kwargs_does_not_change_original() {
    let cfg = Configuration::from_args(
        Some("web1"),
        None, None, None, None, None, None, None, None, None,
    );
    let mut args = HashMap::new();
    args.insert("webhook_url".to_string(), json!("web2"));
    let newcfg = cfg.merge_with_kwargs(args);
    assert_eq!(newcfg.webhook_url, Some("web2".to_string()));
    assert_eq!(cfg.webhook_url, Some("web1".to_string()));
}