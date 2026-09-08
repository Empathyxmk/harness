use crate::forms_builder::forms::{fields, utils};
use crate::forms_builder::forms::settings::{USE_SITES, USE_THREADED_EMAILS, EXTRA_FIELD_TYPES};

#[test]
fn test_field_choices_dict() {
    let choices = "Red\nGreen\nBlue";
    let expected = vec![
        ("Red".to_string(), "Red".to_string()),
        ("Green".to_string(), "Green".to_string()),
        ("Blue".to_string(), "Blue".to_string()),
    ];
    assert_eq!(fields::choices_from_lines(choices), expected);
}

#[test]
fn test_field_choices_dict_empty() {
    assert!(fields::choices_from_lines("").is_empty());
}

#[test]
fn test_is_file() {
    assert!(utils::is_file("photo.PNG"));
    assert!(utils::is_file("document.PDF"));
    assert!(!utils::is_file("example.txt"));
    assert!(!utils::is_file("no_dot"));
}

#[test]
fn test_slugify_strip_and_lower() {
    let s = " Hello__World__ ";
    let sl = utils::slugify(s);
    assert_eq!(sl, "hello--world--");
}

#[test]
fn test_setting_imports() {
    assert!(USE_SITES);
    // The types for USE_SITES etc are already statically checked in Rust.
    assert!(!USE_THREADED_EMAILS);
    assert!(EXTRA_FIELD_TYPES.len() > 0);
}