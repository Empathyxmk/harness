use verbal_expressions::*;
use regex::Regex;

fn assert_not_regex(s: &str, re: &Regex) {
    assert!(!re.is_match(s), "string '{}' should NOT match '{}'", s, re.as_str());
}

#[test]
fn test_should_render_verex_as_string() {
    let mut v = VerEx::new();
    assert_eq!(&*v.add("^$").source(), "^$");
}

#[test]
fn test_should_render_verex_list_as_string() {
    let mut v = VerEx::new();
    let _ = v.add_list(&["^", "[0-9]", "$"]);
    assert_eq!(v.source(), "^[0-9]$");
}

#[test]
fn test_should_match_characters_in_range() {
    let mut v = VerEx::new().start_of_line().range(&["a", "c"]);
    let re = v.regex();
    for character in &["a", "b", "c"] {
        assert!(re.is_match(character));
    }
}

#[test]
fn test_should_not_match_characters_outside_of_range() {
    let mut v = VerEx::new().start_of_line().range(&["a", "c"]);
    let re = v.regex();
    assert_not_regex("d", &re);
}

#[test]
fn test_should_match_characters_in_extended_range() {
    let mut v = VerEx::new().start_of_line().range(&["a", "b", "X", "Z"]);
    let re = v.regex();
    for character in &["a", "b", "X", "Y", "Z"] {
        assert!(re.is_match(character));
    }
}

#[test]
fn test_should_not_match_characters_outside_of_extended_range() {
    let mut v = VerEx::new().start_of_line().range(&["a", "b", "X", "Z"]);
    let re = v.regex();
    assert_not_regex("c", &re);
    assert_not_regex("W", &re);
}

#[test]
fn test_should_match_start_of_line() {
    let mut v = VerEx::new().start_of_line();
    let re = v.regex();
    assert!(re.is_match("text  "), "Not started :(");
}

#[test]
fn test_should_match_end_of_line() {
    let mut v = VerEx::new().start_of_line().end_of_line();
    let re = v.regex();
    assert!(re.is_match(""), "It's not the end!");
}

#[test]
fn test_should_match_anything() {
    let mut v = VerEx::new().start_of_line().anything().end_of_line();
    let re = v.regex();
    assert!(re.is_match("!@#$%¨&*()__+{}"), "Not so anything...");
}

#[test]
fn test_should_match_anything_but_specified_element_when_element_is_not_found() {
    let mut v = VerEx::new().start_of_line().anything_but("X").end_of_line();
    let re = v.regex();
    assert!(re.is_match("Y Files"), "Found the X!");
}

#[test]
fn test_should_not_match_anything_but_specified_element_when_specified_element_is_found() {
    let mut v = VerEx::new().start_of_line().anything_but("X").end_of_line();
    let re = v.regex();
    assert!(!re.is_match("VerEX"), "Didn't found the X :(");
}

#[test]
fn test_should_find_element() {
    let mut v = VerEx::new().start_of_line().find("Wally").end_of_line();
    let re = v.regex();
    assert!(re.is_match("Wally"), "404! Wally not Found!");
}

#[test]
fn test_should_not_find_missing_element() {
    let mut v = VerEx::new().start_of_line().find("Wally").end_of_line();
    let re = v.regex();
    assert!(!re.is_match("Wall-e"), "DAFUQ is Wall-e?");
}

#[test]
fn test_should_match_when_maybe_element_is_present() {
    let mut v = VerEx::new().start_of_line().find("Python2.").maybe("7").end_of_line();
    let re = v.regex();
    assert!(re.is_match("Python2.7"), "Version doesn't match!");
}

#[test]
fn test_should_match_when_maybe_element_is_missing() {
    let mut v = VerEx::new().start_of_line().find("Python2.").maybe("7").end_of_line();
    let re = v.regex();
    assert!(re.is_match("Python2."), "Version doesn't match!");
}

#[test]
fn test_should_match_on_any_when_element_is_found() {
    let mut v = VerEx::new().start_of_line().any("Q").anything().end_of_line();
    let re = v.regex();
    assert!(re.is_match("Query"), "No match found!");
}

#[test]
fn test_should_not_match_on_any_when_element_is_not_found() {
    let mut v = VerEx::new().start_of_line().any("Q").anything().end_of_line();
    let re = v.regex();
    assert!(!re.is_match("W"), "I've found it!");
}

#[test]
fn test_should_match_when_line_break_present() {
    let mut v = VerEx::new().start_of_line().anything().line_break().anything().end_of_line();
    let re = v.regex();
    assert!(re.is_match("Marco \n Polo"), "Give me a break!!");
}

#[test]
fn test_should_match_when_line_break_and_carriage_return_present() {
    let mut v = VerEx::new().start_of_line().anything().line_break().anything().end_of_line();
    let re = v.regex();
    assert!(re.is_match("Marco \r\n Polo"), "Give me a break!!");
}

#[test]
fn test_should_not_match_when_line_break_is_missing() {
    let mut v = VerEx::new().start_of_line().anything().line_break().anything().end_of_line();
    let re = v.regex();
    assert!(!re.is_match("Marco Polo"), "There's a break here!");
}

#[test]
fn test_should_match_when_tab_present() {
    let mut v = VerEx::new().start_of_line().anything().tab().end_of_line();
    let re = v.regex();
    assert!(re.is_match("One tab only\t"), "No tab here!");
}

#[test]
fn test_should_not_match_when_tab_is_missing() {
    let mut v = VerEx::new().start_of_line().anything().tab().end_of_line();
    let re = v.regex();
    assert!(!re.is_match("No tab here"), "There's a tab here!");
}

#[test]
fn test_should_match_when_word_present() {
    let mut v = VerEx::new().start_of_line().anything().word().end_of_line();
    let re = v.regex();
    assert!(re.is_match("Oneword"), "Not just a word!");
}

#[test]
fn test_not_match_when_two_words_are_present_instead_of_one() {
    // Actually tests .tab()! equates to a tab, so:
    let mut v = VerEx::new().start_of_line().anything().tab().end_of_line();
    let re = v.regex();
    assert!(!re.is_match("Two words"), "I've found two of them");
}

#[test]
fn test_should_match_when_or_condition_fulfilled() {
    let mut v = VerEx::new().start_of_line().anything().find("G").OR().find("h").end_of_line();
    let re = v.regex();
    assert!(re.is_match("Github"), "Octocat not found");
}

#[test]
fn test_should_not_match_when_or_condition_not_fulfilled() {
    let mut v = VerEx::new().start_of_line().anything().find("G").OR().find("h").end_of_line();
    let re = v.regex();
    assert!(!re.is_match("Bitbucket"), "Bucket not found");
}

#[test]
fn test_should_match_on_upper_case_when_lower_case_is_given_and_any_case_is_true() {
    let mut v = VerEx::new().start_of_line().find("THOR").end_of_line().with_any_case(true);
    let re = v.regex();
    assert!(re.is_match("thor"), "Upper case Thor, please!");
}

#[test]
fn test_should_match_multiple_lines() {
    let mut v = VerEx::new().start_of_line().anything().find("Pong").anything().end_of_line().search_one_line(true);
    let re = v.regex();
    assert!(re.is_match("Ping \n Pong \n Ping"), "Pong didn't answer");
}

#[test]
fn test_should_match_email_address() {
    let mut v = VerEx::new().start_of_line().word().then("@").word().then(".").word().end_of_line();
    let re = v.regex();
    assert!(re.is_match("mail@mail.com"), "Not a valid email");
}

#[test]
fn test_should_match_url() {
    let mut v = VerEx::new().start_of_line().then("http").maybe("s").then("://").maybe("www.").word().then(".").word().maybe("/").end_of_line();
    let re = v.regex();
    assert!(re.is_match("https://www.google.com/"), "Not a valid email");
}