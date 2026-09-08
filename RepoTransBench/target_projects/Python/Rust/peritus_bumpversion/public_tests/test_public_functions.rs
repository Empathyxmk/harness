use peritus_bumpversion::functions;

#[test]
fn test_replace_numeric_postfix_different_number() {
    assert_eq!(functions::replace_numeric_postfix("abc22xyz", 44), "abc44xyz");
}

#[test]
fn test_replace_numeric_postfix_no_digits() {
    assert_eq!(functions::replace_numeric_postfix("no_digits_here", 9000), "no_digits_here");
}

#[test]
fn test_first_numeric_match_index_new() {
    assert_eq!(functions::first_numeric_match_index("prefix007suffix"), Some((6, 9)));
}

#[test]
fn test_first_numeric_match_index_leading_number() {
    assert_eq!(functions::first_numeric_match_index("99redballoons"), Some((0, 2)));
}

#[test]
fn test_first_alpha_postfix() {
    assert_eq!(functions::first_alpha_postfix("xy3z"), "z");
}

#[test]
fn test_find_first_number_custom_abc9() {
    assert_eq!(functions::find_first_number("ABC9"), "9");
}

#[test]
fn test_find_first_number_custom_a1b2c3() {
    assert_eq!(functions::find_first_number("a1b2c3"), "1");
}

#[test]
fn test_find_first_number_custom_no_digits() {
    assert_eq!(functions::find_first_number("no_digits"), "");
}

#[test]
fn test_increment_string_number_variant() {
    assert_eq!(functions::increment_string_number("hello109world"), "hello110world");
}