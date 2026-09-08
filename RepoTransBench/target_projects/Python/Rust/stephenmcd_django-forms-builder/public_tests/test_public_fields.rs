use crate::forms_builder::forms::fields;

#[test]
fn test_public_field_to_python_boolean_true() {
    let boolean_field = fields::BooleanField;
    assert!(boolean_field.to_python(Some("on")));
}

#[test]
fn test_public_field_to_python_boolean_false() {
    let boolean_field = fields::BooleanField;
    assert!(!boolean_field.to_python(Some("")));
    assert!(!boolean_field.to_python(None));
}

#[test]
fn test_public_field_to_python_select() {
    let select_field = fields::SelectField::new("orange|banana|pear");
    assert_eq!(select_field.choices, vec!["orange", "banana", "pear"]);
}

#[test]
fn test_public_pretty_name_with_number() {
    let result = fields::pretty_name("item_123_value");
    assert_eq!(result, "Item 123 value");
}