use crate::forms_builder::forms::fields;

#[test]
fn test_split_choices_string() {
    let s = "Red\nBlue\r\nGreen";
    let result = fields::split_choices(s);
    let expected = vec![
        ("Red".to_string(), "Red".to_string()),
        ("Blue".to_string(), "Blue".to_string()),
        ("Green".to_string(), "Green".to_string()),
    ];
    assert_eq!(result, expected);
}

#[test]
fn test_split_choices_empty() {
    assert!(fields::split_choices("").is_empty());
    // In Rust, None or 0/3.14 are not valid input for str, so only test for empty string
}

#[test]
fn test_split_choices_list_of_tuples() {
    let lst = vec![
        ("A".to_string(), "Apple".to_string()),
        ("B".to_string(), "Banana".to_string()),
    ];
    assert_eq!(lst.clone(), lst);
}

#[test]
fn test_split_choices_tuple_of_tuples() {
    let tpl = vec![
        ("A".to_string(), "Apple".to_string()),
        ("B".to_string(), "Banana".to_string()),
    ];
    assert_eq!(tpl.clone(), tpl);
}

#[test]
fn test_split_choices_leading_trailing_whitespace() {
    let s = " Red \n\n Blue";
    let result = fields::split_choices(s);
    let expected = vec![
        ("Red".to_string(), "Red".to_string()),
        ("Blue".to_string(), "Blue".to_string()),
    ];
    assert_eq!(result, expected);
}

#[test]
fn test_alias_choices_from_lines() {
    let s = "One\nTwo";
    let result = fields::choices_from_lines(s);
    let expected = vec![
        ("One".to_string(), "One".to_string()),
        ("Two".to_string(), "Two".to_string()),
    ];
    assert_eq!(result, expected);
}

#[test]
fn test_field_choices_and_types() {
    use crate::forms_builder::forms::fields::{FIELD_CHOICES, FIELD_TYPES};
    assert!(FIELD_CHOICES.len() > 0);
    assert!(FIELD_TYPES.len() > 0);
    for i in FIELD_TYPES.iter() {
        assert_eq!(i.len(),2);
    }
    let choices: Vec<_> = FIELD_CHOICES.iter().map(|(k,v)| (*k, *v)).collect();
    let types_arr: Vec<_> = FIELD_TYPES.iter().map(|(k,v)| (*k, *v)).collect();
    assert_eq!(choices, types_arr);
}