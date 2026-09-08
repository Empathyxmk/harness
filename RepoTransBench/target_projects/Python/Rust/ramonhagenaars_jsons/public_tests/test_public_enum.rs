use crate::jsons;
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize, PartialEq)]
enum PublicTestEnum {
    ALPHA = 9,
    BETA = 16,
}

#[test]
fn test_enum_dumps_name() {
    let result = jsons::dumps(&PublicTestEnum::ALPHA);
    assert!(result.contains("ALPHA"));
}

#[test]
fn test_enum_loads_name() {
    let loaded: PublicTestEnum = jsons::load(serde_json::json!("BETA"));
    assert_eq!(loaded, PublicTestEnum::BETA);
}

#[test]
fn test_enum_dump_and_load_name() {
    let dumped = jsons::dumps(&PublicTestEnum::BETA);
    let loaded: PublicTestEnum = jsons::load(serde_json::json!("BETA"));
    assert_eq!(loaded, PublicTestEnum::BETA);
}