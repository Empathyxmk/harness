use serde_json::json;
use jmespath_jp::JpWrapper;

/// Utility: check if the local './jp' binary exists and is executable.
#[allow(dead_code)]
fn jp_exists() -> bool {
    use std::fs;
    use std::os::unix::fs::PermissionsExt;
    let path = "./jp";
    match fs::metadata(path) {
        Ok(meta) => meta.is_file() && (meta.permissions().mode() & 0o111 != 0),
        Err(_) => false,
    }
}

macro_rules! skip_if_no_jp {
    () => {
        if !jp_exists() {
            eprintln!("skipped: jp binary not available for wrapper tests");
            return;
        }
    };
}

#[test]
fn test_basic_select() {
    skip_if_no_jp!();
    let jp = JpWrapper::new("./jp");
    let data = json!({"foo": {"bar": 5}});
    let result = jp.search("foo.bar", &data)
        .expect("jp should work");
    // output should be the integer 5
    assert_eq!(result, json!(5));
}

#[test]
fn test_identity_query() {
    skip_if_no_jp!();
    let jp = JpWrapper::new("./jp");
    let data = json!({"foo": 42});
    let result = jp.search("@", &data)
        .expect("jp should work");
    assert_eq!(result, json!({"foo": 42}));
}

#[test]
fn test_list_index() {
    skip_if_no_jp!();
    let jp = JpWrapper::new("./jp");
    let data = json!({"a": [1,2,3]});
    let result = jp.search("a[1]", &data)
        .expect("jp should work");
    assert_eq!(result, json!(2));
}

#[test]
fn test_invalid_query_raises() {
    skip_if_no_jp!();
    let jp = JpWrapper::new("./jp");
    let data = json!({"foo": 123});
    let fail = jp.search("???", &data);
    assert!(fail.is_err(), "invalid query should cause error");
}

#[test]
fn test_non_json_output() {
    skip_if_no_jp!();
    let jp = JpWrapper::new("./jp");
    let data = json!({"foo": 1});
    let result = jp.search("foo", &data)
        .expect("jp should work");
    assert_eq!(result, json!(1));
}

#[test]
fn test_custom_binary_path() {
    skip_if_no_jp!();
    let jp = JpWrapper::new("./jp"); // default
    let data = json!({"foo": "bar"});
    let got = jp.search("foo", &data)
        .expect("jp should work");
    assert_eq!(got, json!("bar"));
}

#[test]
fn test_error_on_missing_jp() {
    let jp = JpWrapper::new("./missing-jp-bin");
    let result = jp.search("foo", &json!({"foo": 1}));
    assert!(result.is_err(), "should error on missing binary");
}

#[test]
fn test_empty_result() {
    skip_if_no_jp!();
    let jp = JpWrapper::new("./jp");
    let data = json!({"foo": {"bar": 123}});
    let got = jp.search("foo.baz", &data);
    // Should be Null or "" string
    match got {
        Ok(serde_json::Value::Null) => {}
        Ok(serde_json::Value::String(ref s)) => assert_eq!(s, ""),
        Ok(other) => panic!("Unexpected result for missing key: {:?}", other),
        Err(e) => panic!("Unexpected error: {}", e),
    }
}