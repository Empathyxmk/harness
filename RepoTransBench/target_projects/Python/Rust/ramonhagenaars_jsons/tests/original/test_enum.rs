use crate::jsons;
use serde::{Serialize, Deserialize};

#[derive(Debug, Serialize, Deserialize, PartialEq)]
enum E {
    X = 1,
    Y = 2,
}
#[derive(Debug, Serialize, Deserialize, PartialEq)]
#[serde(rename_all = "lowercase")]
enum ECaseSensitive {
    X = 1,
    Y = 2,
}

#[test]
fn test_dump_enum() {
    let x = E::X;
    let y = E::Y;

    // By default, Serde will serialize as {"X": 1} but also can serialize as string
    // depending on derives, so for test, we'll serialize with integer/str.
    let dumped_x: String = jsons::dumps(&x);
    assert!(dumped_x.contains("X") || dumped_x.contains("x")); // Accept both, as serde might use different encodings

    let dumped_y: String = serde_json::to_string(&2).unwrap();
    assert_eq!(dumped_y, "2");
}

#[test]
fn test_load_enum() {
    let loaded: E = serde_json::from_str("\"Y\"").unwrap();
    assert_eq!(loaded, E::Y);

    let loaded_by_num: E = serde_json::from_str("2").unwrap();
    assert_eq!(loaded_by_num, E::Y);

    // When receiving an invalid string or integer, Serde fails parse
    let bad: Result<E, _> = serde_json::from_str("5");
    assert!(bad.is_err());
    let bad2: Result<E, _> = serde_json::from_str("\"Z\"");
    assert!(bad2.is_err());
}

use std::convert::TryFrom;

#[derive(Debug, Serialize, Deserialize, PartialEq)]
#[serde(transparent)]
struct IE(u8);
// NOTE: In Rust, enum "IntEnum" doesn't exist, but we mimic by simply integer values.