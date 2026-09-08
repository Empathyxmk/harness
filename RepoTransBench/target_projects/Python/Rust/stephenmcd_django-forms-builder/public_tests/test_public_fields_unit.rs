use crate::forms_builder::forms::fields;

#[test]
fn test_public_split_choices_diff_input() {
    let value = "red|green|blue";
    let choices = fields::split_choices_delim(value, "|");
    assert_eq!(choices, vec![
        "red".to_string(),
        "green".to_string(),
        "blue".to_string()
    ]);
}

#[test]
fn test_public_pretty_name_diff_input() {
    let val = "zip_code";
    assert_eq!(fields::pretty_name(val), "Zip code");
}

#[test]
fn test_public_is_empty_diff_input() {
    // For Rust, test using Option and String for None and whitespace, plus a Vec for non-empty
    let val: Option<&str> = None;
    assert!(fields::is_empty(&val));
    let vec_val = vec!["value"];
    // Since is_empty only matches Vec<String> or Vec<&str>
    assert!(!fields::is_empty(&vec_val));
    assert!(fields::is_empty(&"      ".to_string()));
}