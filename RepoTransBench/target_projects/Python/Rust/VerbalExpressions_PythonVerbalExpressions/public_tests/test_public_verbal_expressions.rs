use verbal_expressions::*;

fn is_fullmatch(verex: &mut VerEx, s: &str) -> bool {
    match verex.match_string(s) {
        Some(mat) => mat.as_str() == s,
        None => false,
    }
}

#[test]
fn test_public_start_of_line() {
    let mut verex = VerEx::new().start_of_line().then("Begin");
    let s = "BeginAgain";
    let not_s = "NotBegin";
    assert!(verex.is_match(s));
    assert!(!verex.is_match(not_s));
}

#[test]
fn test_public_anything() {
    let mut verex = VerEx::new().anything();
    assert!(verex.is_match("Some string"));
    assert!(verex.is_match(""));
}

#[test]
fn test_public_anything_but() {
    let mut verex = VerEx::new().anything_but("xyz");
    assert!(verex.is_match("Hello world"));
    let m = verex.match_string("xyzworld");
    assert!(m.is_some() && m.unwrap().as_str().is_empty());
}

#[test]
fn test_public_end_of_line() {
    let mut verex = VerEx::new().find("complete").end_of_line();
    assert!(verex.search("mission complete").is_some());
    assert!(verex.match_string("completely done").is_none());
}

#[test]
fn test_public_maybe() {
    let mut verex = VerEx::new().then("red").maybe("car");
    assert!(is_fullmatch(&mut verex, "red"));
    assert!(is_fullmatch(&mut verex, "redcar"));
    assert!(!is_fullmatch(&mut verex, "redcars"));
}

#[test]
fn test_public_any_of() {
    let mut verex = VerEx::new().any("wxyz");
    assert!(verex.is_match("z"));
    assert!(verex.is_match("yell"));
    assert!(!verex.is_match("k"));
}

#[test]
fn test_public_not_of() {
    let mut verex = VerEx::new().anything_but("LMN");
    assert!(verex.is_match("abcde"));
    let m = verex.match_string("MMM");
    assert!(m.is_some() && m.unwrap().as_str().is_empty());
}

#[test]
fn test_public_replace() {
    let mut verex = VerEx::new().find("swap_me");
    let text = "swap_me";
    let result = verex.replace("changed", text);
    assert_eq!(result, "changed");
}