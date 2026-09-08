use crate::jsontool::{expand, restore, is_array_index, convert_json};
use serde_json::json;

#[test]
fn test_string() {
    let s = json!("sss");
    let exp = expand(&s);
    let _s = restore(&exp);
    assert_eq!(s, _s);
}

#[test]
fn test_list() {
    let s = json!(["sss", "ttt", 1, 2, ["3"]]);
    let exp = expand(&s);
    let _s = restore(&exp);
    assert_eq!(s, _s);
}

#[test]
fn test_dict() {
    let s = json!({
        "s": 1,
        "w": 5,
        "t": {
            "m": 0,
            "x": {"y": "z"}
        }
    });
    let exp = expand(&s);
    let _s = restore(&exp);
    assert_eq!(s, _s);
}

#[test]
fn test_complex() {
    let s = json!([
        {"s": 0},
        {"t": ["2", {"x": "z"}]},
        0,
        "w",
        ["x", "g", 1]
    ]);
    let exp = expand(&s);
    let _s = restore(&exp);
    assert_eq!(s[0], _s[0]);
    assert_eq!(s[1], _s[1]);
    assert_eq!(s[2], _s[2]);
    assert_eq!(s[3], _s[3]);
    assert_eq!(s[4], _s[4]);
}

#[test]
fn test_is_array_index() {
    use serde_json::to_value;
    assert!(is_array_index(&vec![json!(0), json!(1), json!(2), json!(3)]));
    assert!(is_array_index(&vec![json!("0"), json!("1"), json!("2"), json!("3")]));
    assert!(is_array_index(&vec![
        json!("0"), json!("1"), json!("10"), json!("2"),
        json!("3"), json!("4"), json!("5"), json!("6"), json!("7"), json!("8"), json!("9")
    ]));
    assert!(!is_array_index(&vec![json!(1), json!(2), json!(3)]));
    assert!(!is_array_index(&vec![json!("0"), json!(1), json!(2)]));
}

#[test]
fn test_unicode() {
    let data = json!([
        {"河流名字": "长江", "河流长度": "6000千米"},
        {"河流名字": "黄河", "河流长度": "5000千米"}
    ]);
    let expobj = expand(&data);
    assert!(expobj.is_object());
}

#[test]
fn test_expand_with_safe() {
    let data = json!({
        "www.a.com": {"qps": 100, "p95": 20},
        "api.a.com": {"qps": 100, "p95": 20, "p99": 100},
    });
    let expobj = expand(&data);
    assert_eq!(expobj["api.a.com.p95"], 20);
    assert_eq!(expobj["api.a.com.p99"], 100);
    let origin = restore(&expobj);
    assert_eq!(origin, data);
}

#[test]
fn test_expand_and_restore() {
    let data = json!(["a", "ab", "b", "a", "ab", "b", "a", "ab", "b", "a", "ab", "b"]);
    let expobj = expand(&data);
    assert_eq!(expobj["0"], "a");
    assert_eq!(expobj["1"], "ab");
    let origin = restore(&expobj);
    assert_eq!(data, origin);
}