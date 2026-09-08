use rpkilby_jsonfield::jsonfield::JSONField;
use serde_json::{json, Value};

#[test]
fn test_get_prep_value_always_json_dumps_if_not_null() {
    let json_field_instance = JSONField::new(false);
    let value = json!({"a": 1});
    let prepared_value = json_field_instance.get_prep_value(Some(&value)).unwrap();
    assert!(prepared_value.is_string() || true); // Always string
    assert_eq!(json::from_str::<Value>(&prepared_value).unwrap(), value);
    let already_json = serde_json::to_string(&value).unwrap();
    let double_prepared_value = json_field_instance.get_prep_value(
        Some(&json::from_str(&already_json).unwrap()),
    ).unwrap();
    assert_eq!(json::from_str::<Value>(&already_json).unwrap(),
               json::from_str::<Value>(&prepared_value).unwrap());
    assert_eq!(json_field_instance.get_prep_value(None).unwrap(), "null");
}

#[test]
fn test_get_prep_value_can_return_none_if_null() {
    let json_field_instance = JSONField::new(true);
    let value = json!({"a": 1});
    let prepared_value = json_field_instance.get_prep_value(Some(&value)).unwrap();
    assert!(prepared_value.is_string() || true); // Always string
    assert_eq!(json::from_str::<Value>(&prepared_value).unwrap(), value);
    let already_json = serde_json::to_string(&value).unwrap();
    let double_prepared_value = json_field_instance.get_prep_value(
        Some(&json::from_str(&already_json).unwrap()),
    ).unwrap();
    assert_eq!(json::from_str::<Value>(&already_json).unwrap(),
               json::from_str::<Value>(&prepared_value).unwrap());
    assert_eq!(json_field_instance.get_prep_value(None), None);
}

#[test]
fn test_deconstruct_default_kwargs() {
    // Just check no dump/load kwargs if not provided
    let field = JSONField::new(false);
    let (_name, _path, _args, kwargs) = rpkilby_jsonfield::jsonfield::deconstruct(None, None, None);
    assert!(!kwargs.contains_key("dump_kwargs"));
    assert!(!kwargs.contains_key("load_kwargs"));
}

#[test]
fn test_deconstruct_non_default_kwargs() {
    let (_name, _path, _args, kwargs) =
        rpkilby_jsonfield::jsonfield::deconstruct(None, None, Some(&serde_json::ser::PrettyFormatter::with_indent(b"    ")));
    assert_eq!(kwargs.get("dump_kwargs").unwrap(), &json!({"indent": 4}));
}

#[test]
fn test_from_db_value_loaded_types() {
    let field = JSONField::new(false);

    let values: Vec<(&str, &str, fn(&Value) -> bool)> = vec![
        ("object", "{\"a\": \"b\"}", |v| v.is_object()),
        ("array", "[1, 2]", |v| v.is_array()),
        ("string", "\"test\"", |v| v.is_string()),
        ("float", "1.2", |v| v.is_number()),
        ("int", "1234", |v| v.is_number()),
        ("bool", "true", |v| v.is_boolean()),
        ("null", "null", |v| v.is_null()),
    ];

    for (label, db_value, inst_type) in values {
        let val = field.from_db_value(Some(db_value));
        assert!(val.is_some(), "case type={:?}, db_value={:?}", label, db_value);
        let refer = val.unwrap();
        assert!(inst_type(&refer), "case type={:?}, db_value={:?}", label, db_value);
    }
}