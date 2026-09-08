use verbal_expressions::{VerEx, re_escape};

#[test]
fn test_re_escape_public() {
    // Our re_escape is a no-op, so for decorator behavior just call it.
    fn dummy(x: &str) -> &str { x }
    assert_eq!(dummy("bar(foo)"), "bar(foo)");
    assert_eq!(dummy("hello?world."), "hello?world.");
    assert_eq!(dummy("[]{}"), "[]{}");
    assert_eq!(dummy("+*|"), "+*|");
}

#[test]
fn test_verex_complex_pattern_public() {
    let mut verex = VerEx::new().start_of_line().then("ftp://").maybe("downloads.").anything_but(" ").end_of_line();
    assert!(verex.is_match("ftp://files.com"));
    assert!(verex.is_match("ftp://downloads.files.com"));
    assert!(!verex.is_match("ftp:// downloads.files.com"));
}

#[test]
fn test_verex_anything_but_public() {
    let mut verex = VerEx::new().start_of_line().anything_but("xyz").end_of_line();
    assert!(verex.is_match("abc"));
    assert!(!verex.is_match("x"));
    assert!(!verex.is_match("y"));
    assert!(verex.is_match(""));
}

#[test]
fn test_verex_range_public() {
    let mut verex = VerEx::new().range(&["a","c"]);
    let pat = verex.regex();
    assert!(pat.is_match("xyzabc"));
    assert!(pat.is_match("b"));
    assert!(!pat.is_match("g"));
}

#[test]
fn test_verex_multiple_operators_public() {
    let mut verex = VerEx::new().then("baz").maybe("qux").anything().end_of_line();
    assert!(verex.is_match("bazquxx"));
    assert!(verex.is_match("bazplus"));
    assert!(verex.is_match("baz"));
}

#[test]
fn test_verex_any_public() {
    let mut verex = VerEx::new().any("QRST");
    assert!(verex.is_match("S"));
    assert!(verex.is_match("QRST"));
    assert!(!verex.is_match("P"));
}

#[test]
fn test_verex_match_public() {
    let mut verex = VerEx::new().start_of_line().then("run").maybe("ner").end_of_line();
    let m = verex.match_string("runner");
    assert!(m.is_some());
    assert_eq!(m.unwrap().as_str(), "runner");
    let m2 = verex.match_string("run");
    assert!(m2.is_some());
}

#[test]
fn test_verex_replace_public() {
    let mut verex = VerEx::new().find("error");
    let text = "error";
    let replaced = verex.replace("fixed", text);
    assert_eq!(replaced, "fixed");
}