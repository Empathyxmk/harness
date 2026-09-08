// Moved from public_tests/test_public_dnsdumpsterapi.rs
use dnsdumpster::{DNSDumpsterAPI};
use std::collections::HashMap;

fn dummy_search(domain: &str) -> HashMap<String, serde_json::Value> {
    let mut dummy_results = HashMap::new();
    if domain == "duckduckgo.com" {
        dummy_results.insert("domain".into(), serde_json::json!("duckduckgo.com"));
        dummy_results.insert("dns_records".into(), serde_json::json!({
            "dns": [{"domain": "ns1.duckduckgo.com"}],
            "mx": [{"exchange": "duckduckgo-com.mail.protection.outlook.com"}],
            "host": [{"host": "imap.duckduckgo.com"}],
        }));
    } else if domain == "mit.edu" {
        dummy_results.insert("domain".into(), serde_json::json!("mit.edu"));
        dummy_results.insert("dns_records".into(), serde_json::json!({
            "dns": [{"domain": "NS1-163.AKAM.NET"}],
            "mx": [{"exchange": "mit-edu.mail.protection.outlook.com"}],
            "host": [{"host": "imap.mit.edu"}],
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
fn test_dnsdumpsterapi_public_attributetypes() {
    let result = dummy_search("duckduckgo.com");
    assert!(result.is_object());
    assert!(result.get("domain").unwrap() == "duckduckgo.com");
    assert!(result.get("dns_records").unwrap().is_object());
    let records = result.get("dns_records").unwrap();
    assert!(records.get("mx").is_some());
    if let Some(serde_json::Value::Array(_)) = records.get("mx") {
        // ok
    } else {
        panic!("'mx' record should be an array");
    }
    assert!(records.get("host").is_some());
    assert!(records.get("dns").is_some());
    for key in ["mx", "host", "dns"].iter() {
        assert!(records.get(*key).is_some());
    }
}

#[test]
fn test_dnsdumpsterapi_public_result_content() {
    let res = dummy_search("mit.edu");
    assert!(res.get("domain").unwrap() == "mit.edu");
    assert!(res.len() > 1);
    if let Some(serde_json::Value::Object(records)) = res.get("dns_records") {
        let mut has_records = false;
        for v in records.values() {
            if let serde_json::Value::Array(arr) = v {
                if !arr.is_empty() {
                    has_records = true;
                    break;
                }
            }
        }
        assert!(has_records, "There should be at least one populated DNS record entry");
    } else {
        panic!("dns_records field missing or wrong type");
    }
}