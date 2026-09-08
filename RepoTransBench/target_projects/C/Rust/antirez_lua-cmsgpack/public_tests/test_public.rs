//! Translated from test_public.lua -- public interface/value tests

use lua_cmsgpack as cmsgpack;
use serde_json::{json, Value};

#[test]
fn test_pack_unpack_unsigned_int_large() {
    let value = 123456i64;
    let encoded = cmsgpack::pack(value).expect("Pack uint failed");
    let decoded: i64 = cmsgpack::unpack(&encoded).expect("Unpack uint failed");
    assert_eq!(decoded, value);
}

#[test]
fn test_pack_unpack_negative_int() {
    let value = -78901i64;
    let encoded = cmsgpack::pack(value).expect("Pack negative int failed");
    let decoded: i64 = cmsgpack::unpack(&encoded).expect("Unpack negative int failed");
    assert_eq!(decoded, value);
}

#[test]
fn test_pack_unpack_positive_float() {
    let value = 42.4242f64;
    let encoded = cmsgpack::pack(value).expect("Pack float failed");
    let decoded: f64 = cmsgpack::unpack(&encoded).expect("Unpack float failed");
    assert!((decoded - value).abs() < 1e-10);
}

#[test]
fn test_pack_unpack_negative_float() {
    let value = -100.5f64;
    let encoded = cmsgpack::pack(value).expect("Pack neg float failed");
    let decoded: f64 = cmsgpack::unpack(&encoded).expect("Unpack neg float failed");
    assert!((decoded - value).abs() < 1e-10);
}

#[test]
fn test_pack_unpack_string_different() {
    let value = "public test string";
    let encoded = cmsgpack::pack(value).expect("Pack str failed");
    let decoded: String = cmsgpack::unpack(&encoded).expect("Unpack str failed");
    assert_eq!(decoded, value);
}

#[test]
fn test_pack_unpack_unicode_string() {
    let value = "🚀🔬π🌍";
    let encoded = cmsgpack::pack(value).expect("Pack unicode str failed");
    let decoded: String = cmsgpack::unpack(&encoded).expect("Unpack unicode str failed");
    assert_eq!(decoded, value);
}

#[test]
fn test_pack_unpack_large_table() {
    let value: Vec<i32> = (1..=100).map(|i| i*2).collect();
    let encoded = cmsgpack::pack(&value).expect("Pack vec failed");
    let decoded: Vec<i32> = cmsgpack::unpack(&encoded).expect("Unpack vec failed");
    assert_eq!(decoded.len(), 100);
    for (i, v) in decoded.iter().enumerate() {
        assert_eq!(*v, (i+1) as i32 * 2);
    }
}

#[test]
fn test_pack_unpack_table_string_keys() {
    use std::collections::HashMap;
    let mut value = HashMap::new();
    value.insert("foo", 100);
    value.insert("bar", 200);
    value.insert("baz", 300);
    let encoded = cmsgpack::pack(&value).expect("Pack map failed");
    let decoded: HashMap<String, i32> = cmsgpack::unpack(&encoded).expect("Unpack map failed");
    assert_eq!(*decoded.get("foo").unwrap(), 100);
    assert_eq!(*decoded.get("bar").unwrap(), 200);
    assert_eq!(*decoded.get("baz").unwrap(), 300);
}

#[test]
fn test_pack_unpack_nested_tables() {
    #[derive(Debug, serde::Serialize, serde::Deserialize, PartialEq)]
    struct Deep {
        alpha: Alpha,
        delta: i32,
    }
    #[derive(Debug, serde::Serialize, serde::Deserialize, PartialEq)]
    struct Alpha {
        beta: Beta,
    }
    #[derive(Debug, serde::Serialize, serde::Deserialize, PartialEq)]
    struct Beta {
        gamma: i32,
    }
    let value = Deep {
        alpha: Alpha {
            beta: Beta { gamma: 9876 },
        },
        delta: 123,
    };
    let encoded = cmsgpack::pack(&value).expect("Pack nested failed");
    let decoded: Deep = cmsgpack::unpack(&encoded).expect("Unpack nested failed");
    assert_eq!(decoded, value);
}

#[test]
fn test_pack_unpack_array_of_strings() {
    let value = vec!["a", "b", "c", "d"];
    let encoded = cmsgpack::pack(&value).expect("Pack str-array failed");
    let decoded: Vec<String> = cmsgpack::unpack(&encoded).expect("Unpack str-array failed");
    assert_eq!(decoded, value);
}

#[test]
fn test_pack_unpack_true_false() {
    let encoded_true = cmsgpack::pack(true).expect("Pack true failed");
    let decoded_true: bool = cmsgpack::unpack(&encoded_true).expect("Unpack true failed");
    assert!(decoded_true);
    let encoded_false = cmsgpack::pack(false).expect("Pack false failed");
    let decoded_false: bool = cmsgpack::unpack(&encoded_false).expect("Unpack false failed");
    assert!(!decoded_false);
}

#[test]
fn test_pack_unpack_nil() {
    let encoded = cmsgpack::pack(serde_json::Value::Null).expect("Pack nil failed");
    let decoded: Value = cmsgpack::unpack(&encoded).expect("Unpack nil failed");
    assert_eq!(decoded, Value::Null);
}