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

macro_rules! skip_if_no_jp_public {
    () => {
        if !jp_exists() {
            eprintln!("skipped: jp binary not available for wrapper tests (public)");
            return;
        }
    };
}

#[test]
fn test_public_basic_select() {
    skip_if_no_jp_public!();
    let jp = JpWrapper::new("./jp");
    let data = json!({"alpha": {"beta": 9}});
    let result = jp.search("alpha.beta", &data)
        .expect("jp should work");
    assert_eq!(result, json!(9));
}

#[test]
fn test_public_identity_query() {
    skip_if_no_jp_public!();
    let jp = JpWrapper::new("./jp");
    let data = json!({"bar": 17});
    let result = jp.search("@", &data)
        .expect("jp should work");
    assert_eq!(result, json!({"bar": 17}));
}

#[test]
fn test_public_list_index() {
    skip_if_no_jp_public!();
    let jp = JpWrapper::new("./jp");
    let data = json!({"numbers": [10, 20, 30]});
    let result = jp.search("numbers[2]", &data)
        .expect("jp should work");
    assert_eq!(result, json!(30));
}

#[test]
fn test_public_invalid_query_raises() {
    skip_if_no_jp_public!();
    let jp = JpWrapper::new("./jp");
    let data = json!({"bar": 987});
    let fail = jp.search("!!!", &data);
    assert!(fail.is_err(), "invalid query should error");
}

#[test]
fn test_public_non_json_output() {
    skip_if_no_jp_public!();
    let jp = JpWrapper::new("./jp");
    let data = json!({"bar": 7});
    let result = jp.search("bar", &data)
        .expect("jp should work");
    assert_eq!(result, json!(7));
}

#[test]
fn test_public_custom_binary_path() {
    skip_if_no_jp_public!();
    let jp = JpWrapper::new("./jp"); // default
    let data = json!({"a": "b"});
    let got = jp.search("a", &data)
        .expect("jp should work");
    assert_eq!(got, json!("b"));
}

#[test]
fn test_public_error_on_missing_jp() {
    let jp = JpWrapper::new("./not-found-jp-bin");
    let result = jp.search("bar", &json!({"bar": 4}));
    assert!(result.is_err(), "should error on missing binary");
}

#[test]
fn test_public_empty_result() {
    skip_if_no_jp_public!();
    let jp = JpWrapper::new("./jp");
    let data = json!({"alpha": {"beta": 1234}});
    let got = jp.search("alpha.gamma", &data);
    // Should be Null or "" string
    match got {
        Ok(serde_json::Value::Null) => {}
        Ok(serde_json::Value::String(ref s)) => assert_eq!(s, ""),
        Ok(other) => panic!("Unexpected result for missing key: {:?}", other),
        Err(e) => panic!("Unexpected error: {}", e),
    }
}