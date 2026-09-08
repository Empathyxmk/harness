use crate::forms_builder::forms::fields;
#[test]
fn test_linebreak_re() {
    let s = "a\nb";
    let out: Vec<&str> = fields::linebreak_re().split(s).collect();
    assert_eq!(out, vec!["a", "b"]);
    let s2 = "a\r\nb";
    let out2: Vec<&str> = fields::linebreak_re().split(s2).collect();
    assert_eq!(out2, vec!["a", "b"]);
    let s3 = "a\r\nb\nc";
    let out3: Vec<&str> = fields::linebreak_re().split(s3).collect();
    assert_eq!(out3, vec!["a", "b", "c"]);
}

#[test]
fn test_field_type_iterable() {
    let types_list = fields::FIELD_TYPES;
    assert!(types_list.len() > 0);
    for t in types_list {
        assert_eq!(t.len(), 2);
    }
}

#[test]
fn test_choices_from_lines_basic() {
    let choices = "Red\nGreen\nBlue";
    let expected = vec![
        ("Red".to_string(), "Red".to_string()),
        ("Green".to_string(), "Green".to_string()),
        ("Blue".to_string(), "Blue".to_string()),
    ];
    assert_eq!(fields::choices_from_lines(choices), expected);
}

#[test]
fn test_choices_from_lines_empty() {
    assert!(fields::choices_from_lines("").is_empty());
    assert!(fields::choices_from_lines("     ").is_empty());
    // Handles basic list/tuple pass-through
    let out = vec![("foo".to_string(), "foo".to_string())];
    assert_eq!(out, vec![("foo".to_string(), "foo".to_string())]);
}