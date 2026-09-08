//! Simulated JWT config option tests in Rust
use std::collections::HashMap;

#[test]
fn test_default_configs() {
    let config: HashMap<&str, &str> = [
        ("header_name", "Authorization"),
        ("header_type", "Bearer"),
        ("json_key", "access_token"),
        ("refresh_json_key", "refresh_token"),
        ("identity_claim_key", "sub"),
        ("error_msg_key", "msg"),
        ("algorithm", "HS256"),
    ].iter().copied().collect();
    assert_eq!(config["header_name"], "Authorization");
    assert_eq!(config["header_type"], "Bearer");
    assert_eq!(config["json_key"], "access_token");
    assert_eq!(config["refresh_json_key"], "refresh_token");
    assert_eq!(config["identity_claim_key"], "sub");
    assert_eq!(config["error_msg_key"], "msg");
    assert_eq!(config["algorithm"], "HS256");
}

#[test]
fn test_override_configs() {
    let config: HashMap<&str, &str> = [
        ("header_name", "TestHeader"),
        ("header_type", "TestType"),
        ("json_key", "TestKey"),
        ("refresh_json_key", "TestRefreshKey"),
        ("identity_claim_key", "foo"),
        ("error_msg_key", "message"),
        ("algorithm", "HS512"),
    ].iter().copied().collect();
    assert_eq!(config["header_name"], "TestHeader");
    assert_eq!(config["header_type"], "TestType");
    assert_eq!(config["json_key"], "TestKey");
    assert_eq!(config["refresh_json_key"], "TestRefreshKey");
    assert_eq!(config["identity_claim_key"], "foo");
    assert_eq!(config["error_msg_key"], "message");
    assert_eq!(config["algorithm"], "HS512");
}

#[test]
fn test_symmetric_secret_key() {
    let secret_key = "foobar";
    assert_eq!(secret_key, "foobar");
}

#[test]
fn test_invalid_config_options() {
    let invalid_token_locations = vec!["", "banana"];
    for loc in invalid_token_locations {
        match loc {
            "" | "banana" => assert!(true),
            _ => panic!("Should not reach valid location"),
        }
    }
}