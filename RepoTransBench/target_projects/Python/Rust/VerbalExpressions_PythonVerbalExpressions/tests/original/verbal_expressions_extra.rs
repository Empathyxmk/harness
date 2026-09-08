use verbal_expressions::*;
use regex::Regex;

#[test]
fn test_anything() {
    let mut v = VerEx::new().anything();
    let re = v.regex();
    assert!(re.is_match("abcdef"));
}

#[test]
fn test_anything_but() {
    let mut v = VerEx::new().anything_but("x");
    let re = v.regex();
    assert!(re.is_match("abc"));
    assert!(re.is_match(""));
    let mut v2 = VerEx::new().anything_but("x");
    let re2 = v2.regex();
    // "x" as whole string shouldn't match
    assert!(re2.full_match("x").is_none());
    assert!(re.is_match("abcdef"));
}

#[test]
fn test_end_of_line() {
    let mut v = VerEx::new().end_of_line();
    let s = "end$";
    let pat = format!("{}$", v.source());
    let re = Regex::new(&pat).unwrap();
    assert!(re.is_match(s));
}

#[test]
fn test_maybe() {
    let mut v = VerEx::new().maybe("abc");
    let re = v.regex();
    assert!(re.is_match("abc"));
    assert!(re.is_match(""));
}

#[test]
fn test_start_of_line() {
    let mut v = VerEx::new().start_of_line();
    let pattern = v.source();
    assert!(pattern.starts_with("^"));
}

#[test]
fn test_find_and_then() {
    let mut v = VerEx::new().find("cat");
    let re = v.regex();
    assert!(re.is_match("cat"));
    let mut v2 = VerEx::new().then("dog");
    let re2 = v2.regex();
    assert!(re2.is_match("dog"));
}

#[test]
fn test_any_any_of() {
    let mut v = VerEx::new().any("abc");
    let re = v.regex();
    assert!(re.is_match("a"));
    assert!(re.is_match("b"));
    assert!(!re.is_match("d"));
    let mut v2 = VerEx::new().any_of("xyz");
    let re2 = v2.regex();
    assert!(re2.is_match("z"));
}

#[test]
fn test_line_break_br() {
    let mut v = VerEx::new().line_break();
    let re = v.regex();
    assert!(re.is_match("\n"));
    assert!(re.is_match("\r\n"));
    let mut v2 = VerEx::new().br();
    let re2 = v2.regex();
    assert!(re2.is_match("\n"));
}

#[test]
fn test_range_with_odd_args() {
    let mut v = VerEx::new().range(&["a", "c", "0", "1"]);
    let re = v.regex();
    assert!(re.is_match("a"));
    assert!(re.is_match("b"));
    assert!(re.is_match("c"));
    assert!(re.is_match("0"));
    assert!(re.is_match("1"));
}

#[test]
fn test_tab_and_word() {
    let mut v = VerEx::new().tab();
    let re = v.regex();
    assert!(re.is_match("\t"));
    let mut w = VerEx::new().word();
    let re2 = w.regex();
    assert!(re2.is_match("wordtest"));
}

#[test]
fn test_or_without_value() {
    let mut v = VerEx::new().find("foo").OR();
    let src = v.source();
    assert!(src.contains("|"));
    // In Rust, VerEx always has find method (no runtime hasattr check)
}

#[test]
fn test_or_with_value() {
    let mut v = VerEx::new().find("foo").OR_with("bar");
    let src = v.source();
    assert!(src.contains("|(bar)"));
}

#[test]
fn test_replace() {
    let mut v = VerEx::new().find("foo");
    let result = v.replace("bar", "foofoo");
    assert_eq!(result, "barbar");
}

#[test]
fn test_with_any_case() {
    let mut v = VerEx::new().find("abc").with_any_case(true);
    assert_eq!(*v.modifiers.get(&'i').unwrap_or(&false), true);
    v.with_any_case(false);
    assert_eq!(*v.modifiers.get(&'i').unwrap_or(&false), false);
}

#[test]
fn test_search_one_line() {
    let mut v = VerEx::new().search_one_line(true);
    assert_eq!(*v.modifiers.get(&'m').unwrap_or(&false), true);
    v.search_one_line(false);
    assert_eq!(*v.modifiers.get(&'m').unwrap_or(&false), false);
}

#[test]
fn test_with_ascii() {
    let mut v = VerEx::new().with_ascii(true);
    assert_eq!(*v.modifiers.get(&'a').unwrap_or(&false), true);
    v.with_ascii(false);
    assert_eq!(*v.modifiers.get(&'a').unwrap_or(&false), false);
}

#[test]
fn test_value_and_source() {
    let mut v = VerEx::new().find("cat");
    assert_eq!(v.value(), v.source());
    assert_eq!(v.raw(), v.source());
}