//! Translated from test_lua_extra_public.lua -- public extra/edge case tests

use lua_cmsgpack as cmsgpack;
use serde_json::{json, Value};

#[test]
fn test_nil_roundtrip_public() {
    let encoded = cmsgpack::pack(serde_json::Value::Null).expect("Failed to pack nil");
    assert!(!encoded.is_empty());
    let decoded: Value = cmsgpack::unpack(&encoded).expect("Failed to unpack nil");
    assert_eq!(decoded, Value::Null);
}

#[test]
fn test_bool_roundtrip_public() {
    for v in [true, false].iter() {
        let encoded = cmsgpack::pack(*v).expect("Pack bool failed");
        let decoded: bool = cmsgpack::unpack(&encoded).expect("Unpack bool failed");
        assert_eq!(*v, decoded);
    }
}

#[test]
fn test_number_boundaries_public() {
    let test_numbers: Vec<Value> = vec![
        json!(11), json!(202), json!(-303), json!(1024), json!(4096), json!(-8192),
        json!(256), json!(-256), json!((1<<24)-100), json!(-(1<<24)+20),
        json!(76.23), json!(-0.99)
    ];
    for n in test_numbers {
        let encoded = cmsgpack::pack(&n).expect("Pack number failed");
        let decoded: Value = cmsgpack::unpack(&encoded).expect("Unpack number failed");
        assert_eq!(decoded, n, "Failed roundtrip for number {}", n);
    }
}

#[test]
fn test_empty_and_long_string_public() {
    let s = String::new();
    let encoded = cmsgpack::pack(&s).expect("Pack empty string failed");
    assert!(!encoded.is_empty());
    let decoded: String = cmsgpack::unpack(&encoded).expect("Unpack empty string failed");
    assert_eq!(decoded, "");

    let s = "Z".repeat(512);
    let encoded = cmsgpack::pack(&s).expect("Pack long string failed");
    let decoded: String = cmsgpack::unpack(&encoded).expect("Unpack long string failed");
    assert_eq!(decoded, s);
}

#[test]
fn test_table_empty_public() {
    let tbl: Vec<Value> = vec![];
    let encoded = cmsgpack::pack(&tbl).expect("Pack empty vec(table) failed");
    let decoded: Vec<Value> = cmsgpack::unpack(&encoded).expect("Unpack empty vec(table) failed");
    assert!(decoded.is_empty());
}

#[test]
fn test_table_mix_keys_public() {
    use std::collections::HashMap;
    #[derive(serde::Serialize, serde::Deserialize, Debug)]
    struct MixKeys {
        one: i32,
        #[serde(rename = "@two#")]
        at_two: i32,
        #[serde(rename = "space key")]
        space_key: i32,
        #[serde(rename = "4")]
        four: i32,
    }
    let value = MixKeys {
        one: 11,
        at_two: 22,
        space_key: 33,
        four: 44,
    };
    let encoded = cmsgpack::pack(&value).expect("Pack mix keys failed");
    // decode as Value to check keys
    let decoded: Value = cmsgpack::unpack(&encoded).expect("Unpack mix keys failed");
    assert_eq!(decoded["one"], 11);
    assert_eq!(decoded["@two#"], 22);
    assert_eq!(decoded["space key"], 33);
    assert_eq!(decoded["4"], 44);
}

#[test]
fn test_nested_long_table_public() {
    #[derive(serde::Serialize, serde::Deserialize, Debug)]
    struct TableInput {
        sub: Sub,
        final_: String,
        values: Vec<i32>,
    }
    #[derive(serde::Serialize, serde::Deserialize, Debug)]
    struct Sub {
        subsub: SubSub,
    }
    #[derive(serde::Serialize, serde::Deserialize, Debug)]
    struct SubSub {
        xxx: i32,
        y: i32,
    }
    let obj = TableInput {
        sub: Sub { subsub: SubSub { xxx: 99, y: 10 } },
        final_: "END".to_string(),
        values: vec![1000, 2000, 3000, 4000],
    };
    let encoded = cmsgpack::pack(&obj).expect("Pack nested table failed");
    let decoded: Value = cmsgpack::unpack(&encoded).expect("Unpack nested table failed");
    assert_eq!(decoded["final"], "END");
    assert_eq!(decoded["values"].as_array().unwrap().len(), 4);
    assert_eq!(decoded["sub"]["subsub"]["xxx"], 99);
    assert_eq!(decoded["sub"]["subsub"]["y"], 10);
}

#[test]
fn test_array_table_with_holes_public() {
    use serde_json::json;
    let mut arr = serde_json::Map::new();
    arr.insert("1".to_string(), json!("A"));
    arr.insert("2".to_string(), json!(false));
    arr.insert("4".to_string(), json!("B"));
    let value = Value::Object(arr);
    let encoded = cmsgpack::pack(&value).expect("Pack array with holes failed");
    let decoded: Value = cmsgpack::unpack(&encoded).expect("Unpack array with holes failed");
    assert_eq!(decoded["1"], "A");
    assert_eq!(decoded["2"], false);
    assert_eq!(decoded["4"], "B");
}