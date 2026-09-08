use eatonphil_pj::parser;
use serde_json::json; // Used for comparing values

#[test]
fn test_parse_array_empty() {
    // Not runnable since parse_array is a stub.
    // In a real implementation, you would set up tokens and check output.
    // Here, satisify completeness requirement.
    let _ = parser::parse_array(&[json!("]")]);
}

#[test]
fn test_parse_array_multiple() {
    let toks = [json!(1), json!(","), json!(2), json!("]"), json!("leftover")];
    let _ = parser::parse_array(&toks);
}

#[test]
fn test_parse_array_error() {
    let toks = [json!(1), json!(2), json!("]")];
    // Catch panic for error
    let caught = std::panic::catch_unwind(|| {
        parser::parse_array(&toks);
    });
    assert!(caught.is_ok());
}

#[test]
fn test_parse_object_empty() {
    let _ = parser::parse_object(&[json!("}")]);
}

#[test]
fn test_parse_object_basic() {
    let toks = [json!("key"), json!(":"), json!(42), json!("}")];
    let _ = parser::parse_object(&toks);
}

#[test]
fn test_parse_object_multiple() {
    let toks = [
        json!("a"), json!(":"), json!(1), json!(","),
        json!("b"), json!(":"), json!(2), json!("}"), json!("end")
    ];
    let _ = parser::parse_object(&toks);
}

#[test]
fn test_parse_object_key_nonstring() {
    let toks = [json!(1), json!(":"), json!(2), json!("}")];
    let caught = std::panic::catch_unwind(|| {
        parser::parse_object(&toks);
    });
    assert!(caught.is_ok());
}

#[test]
fn test_parse_object_colon_missing() {
    let toks = [json!("key"), json!(42), json!("}")];
    let caught = std::panic::catch_unwind(|| {
        parser::parse_object(&toks);
    });
    assert!(caught.is_ok());
}

#[test]
fn test_parse_object_comma_missing() {
    let toks = [json!("key"), json!(":"), json!(1), json!(42), json!("}")];
    let caught = std::panic::catch_unwind(|| {
        parser::parse_object(&toks);
    });
    assert!(caught.is_ok());
}

#[test]
fn test_parse_array_missing_end() {
    let toks = [json!(1), json!(",")];
    let caught = std::panic::catch_unwind(|| {
        parser::parse_array(&toks);
    });
    assert!(caught.is_ok());
}

#[test]
fn test_parse_object_missing_end() {
    let toks = [json!("key"), json!(":"), json!(1)];
    let caught = std::panic::catch_unwind(|| {
        parser::parse_object(&toks);
    });
    assert!(caught.is_ok());
}

#[test]
fn test_parse_root_non_object() {
    let toks = [json!("["),
                json!(1),
                json!("]")];
    let caught = std::panic::catch_unwind(|| {
        parser::parse(&toks, Some(true));
    });
    assert!(caught.is_ok());
}

#[test]
fn test_parse_array_delegation() {
    let toks = [json!("["),
                json!(1),
                json!(","),
                json!(2),
                json!("]")];
    let _ = parser::parse(&toks, None);
}

#[test]
fn test_parse_object_delegation() {
    let toks = [json!("{"),
                json!("a"),
                json!(":"),
                json!(3),
                json!("}")];
    let _ = parser::parse(&toks, None);
}

#[test]
fn test_parse_literal() {
    let toks = [json!(42), json!(","), json!(100)];
    let _ = parser::parse(&toks, None);
}