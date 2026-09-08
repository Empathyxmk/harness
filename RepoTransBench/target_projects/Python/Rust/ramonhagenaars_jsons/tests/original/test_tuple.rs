use crate::jsons;
use chrono::{DateTime, Utc, TimeZone};
use serde::{Serialize, Deserialize};

#[test]
fn test_dump_tuple() {
    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    struct NestedTuple(DateTime<Utc>);
    let dat = Utc.ymd(2018, 7, 8).and_hms(21, 34, 0);
    let tup = (1, 2, 3, vec![4, 5, (dat,)]);

    let dumped = jsons::dump(&tup);
    let date_str = dat.to_rfc3339_opts(chrono::SecondsFormat::Secs, true);
    let expected = serde_json::json!([1, 2, 3, [4, 5, [date_str]]]);
    assert_eq!(dumped, expected);
}

#[test]
fn test_dump_namedtuple() {
    #[derive(Debug, Serialize, Deserialize, PartialEq)]
    struct T { x: u8, y: u8 }
    let t = T { x: 1, y: 2 };
    let dumped = jsons::dump(&t);
    assert_eq!(dumped, serde_json::json!({"x":1,"y":2}));
}

#[test]
fn test_load_tuple_typing() {
    let tuple_val = (1, "2", 3.0f32);
    let json = serde_json::json!([1, "2", 3.0]);
    let loaded: (i32, String, f32) = serde_json::from_value(json).unwrap();
    assert_eq!(tuple_val, loaded);
}