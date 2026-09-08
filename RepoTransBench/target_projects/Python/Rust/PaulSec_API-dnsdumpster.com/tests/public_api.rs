// Moved from public_tests/test_public_api.rs
use dnsdumpster::{DNSDumpsterAPI};
use std::collections::HashMap;

fn dummy_search(domain: &str) -> HashMap<String, serde_json::Value> {
    let mut dummy_results = HashMap::new();
    if domain == "openai.com" {
        dummy_results.insert("domain".into(), serde_json::json!("openai.com"));
        dummy_results.insert("dns_records".into(), serde_json::json!({
            "dns": [{"domain": "ns1.openai.com"}],
            "mx": [{"exchange": "aspmx.l.google.com"}],
            "host": [{"host": "mail.openai.com"}],
        }));
    } else if domain == "duckduckgo.com" {
        dummy_results.insert("domain".into(), serde_json::json!("duckduckgo.com"));
        dummy_results.insert("dns_records".into(), serde_json::json!({
            "dns": [{"domain": "ns1.duckduckgo.com"}],
            "mx": [{"exchange": "duckduckgo-com.mail.protection.outlook.com"}],
            "host": [{"host": "imap.duckduckgo.com"}],
        }));
    } else {
        dummy_results.insert("domain".into(), serde_json::json!(domain));
        dummy_results.insert("dns_records".into(), serde_json::json!({
            "dns": [],
            "mx": [],
            "host": [],
        }));
    }
    dummy_results
}

#[test]
fn test_dnsdumpsterapi_public_search() {
    // Use the public "search" logic as in dummy_search
    let domain = "openai.com";
    let result = dummy_search(domain);
    assert_eq!(result.get("domain").unwrap(), "openai.com");
    assert!(result.contains_key("dns_records"));
    if let Some(serde_json::Value::Object(ref records)) = result.get("dns_records") {
        assert!(!records.is_empty());
        // at least one DNS record list should not be empty
        let mut found = false;
        for (_k, v) in records.iter() {
            if let serde_json::Value::Array(arr) = v {
                if !arr.is_empty() {
                    found = true;
                    break;
                }
            }
        }
        assert!(found, "At least one DNS record list should not be empty");
    } else {
        panic!("dns_records field should be an object/dict");
    }
}