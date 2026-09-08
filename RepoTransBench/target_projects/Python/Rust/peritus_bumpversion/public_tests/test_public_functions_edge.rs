use peritus_bumpversion::functions;

#[test]
fn test_replace_numeric_postfix_only_number() {
    assert_eq!(functions::replace_numeric_postfix("667", 334), "334");
}

#[test]
fn test_first_numeric_match_index_none_number() {
    assert_eq!(functions::first_numeric_match_index("qwerty"), None);
}

#[test]
fn test_first_alpha_postfix_edge() {
    assert_eq!(functions::first_alpha_postfix("123456"), "");
}

#[test]
fn test_find_first_number_complex_string() {
    let val = "xy_hello2abc5";
    assert_eq!(functions::find_first_number(val), "2");
}

#[test]
fn test_increment_string_number_only_number() {
    assert_eq!(functions::increment_string_number("105"), "106");
}

#[test]
fn test_increment_string_number_with_zeros() {
    assert_eq!(functions::increment_string_number("code007bond"), "code008bond");
}