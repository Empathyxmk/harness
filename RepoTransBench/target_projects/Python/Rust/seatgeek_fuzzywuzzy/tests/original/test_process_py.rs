use seatgeek_fuzzywuzzy::process;

#[test]
fn test_extract_one() {
    let choices = vec!["new york jets", "new york giants", "liverpool"];
    let query = "new york jets";
    let res = process::extract_one(query, choices.iter().map(|x| *x));
    assert!(res.is_some());
    let (s, _) = res.unwrap();
    assert_eq!(s, "new york jets");
}

#[test]
fn test_extract_limit_and_processor() {
    // processor not used, pass None
    let choices = vec!["foo Xbar", "bar", "baz"];
    let query = "foo bar";
    let res = process::extract(query, choices.iter().map(|x| *x), None, None, Some(2));
    assert_eq!(res.len(), 0); // None should contain 'foo bar' as substring
}

#[test]
fn test_extract_none() {
    let res = process::extract_one("", Vec::<&str>::new().iter().map(|x| *x));
    assert!(res.is_none());
    let res = process::extract("", Vec::<&str>::new().iter().map(|x| *x), None, None, None);
    assert_eq!(res.len(), 0);
}

#[test]
fn test_empty_choices_extract_one() {
    let res = process::extract_one("a", Vec::<&str>::new().iter().map(|x| *x));
    assert!(res.is_none());
    let res = process::extract("a", Vec::<&str>::new().iter().map(|x| *x), None, None, None);
    assert_eq!(res.len(), 0);
}

#[test]
fn test_indexed_choices() {
    // Only works for lists in this implementation.
    let choices = vec!["foo", "boo"];
    let res = process::extract_one("foo", choices.iter().map(|x| *x));
    assert!(res.is_some());
    let (match_s, _) = res.unwrap();
    assert_eq!(match_s, "foo");
}