use rpkilby_jsonfield::jsonfield::{JSONField, deconstruct};
use serde_json::json;

#[test]
fn test_deconstruct_non_default_kwargs() {
    let (_name, _path, _args, kwargs) = deconstruct(Some("str"), Some("str"), Some(&serde_json::ser::PrettyFormatter::with_indent(b"    ")));
    assert_eq!(kwargs.get("dump_kwargs").unwrap(), &json!({"indent": 4}));
}

#[test]
fn test_deconstruct_default_kwargs() {
    let (_name, _path, _args, kwargs) = deconstruct(None, None, None);
    assert!(!kwargs.contains_key("decoder_class"));
    assert!(!kwargs.contains_key("encoder_class"));
    assert!(!kwargs.contains_key("dump_kwargs"));
}

#[test]
fn test_get_prep_value_can_return_none_if_null() {
    let field = JSONField::new(true);
    let val = field.get_prep_value(None);
    assert_eq!(val, None);
}

#[test]
fn test_get_prep_value_always_json_dumps_if_not_null() {
    let field = JSONField::new(true);
    let obj = json!({"number": 33, "flag": false});
    let val = field.get_prep_value(Some(&obj));
    assert_eq!(&val.unwrap(), "{\"number\":33,\"flag\":false}");
}

#[test]
fn test_from_db_value_loaded_types() {
    let field = JSONField::new(false);

    let obj = field.from_db_value(Some("{\"z\":1}"));
    assert_eq!(obj, Some(json!({"z": 1})));

    let obj_none = field.from_db_value(None);
    assert_eq!(obj_none, None);
}