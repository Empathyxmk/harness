use std::io::Cursor;

use crate::runner::path_to_enlightenment::*;

#[test]
fn test_empty_input_produces_empty_output() {
    let infile = Cursor::new(b"");
    let expected: Vec<String> = vec![];
    let received = filter_koan_names(infile);
    assert_eq!(expected, received);
}

#[test]
fn test_names_yielded_match_names_in_file() {
    let names = ["this.is.a.test", "this.is.only.a.test"];
    let joined = names.join("\n");
    let infile = Cursor::new(joined.as_bytes());
    let received = filter_koan_names(infile);
    let expected: Vec<String> = names.iter().map(|&s| s.to_string()).collect();
    assert_eq!(expected, received);
}

#[test]
fn test_whitespace_is_stripped() {
    let names = [
        "this.is.a.test",
        "    white.space.should.be.stripped",
        "this.is.only.a.test",
        "white.space.should.be.stripped    ",
    ];
    let infile = Cursor::new(names.join("\n").as_bytes());
    let expected = vec![
        "this.is.a.test",
        "white.space.should.be.stripped",
        "this.is.only.a.test",
        "white.space.should.be.stripped",
    ];
    let received = filter_koan_names(infile);
    let expected: Vec<String> = expected.iter().map(|s| s.to_string()).collect();
    assert_eq!(expected, received);
}

#[test]
fn test_commented_out_names_are_excluded() {
    let names = [
        "this.is.a.test",
        "#this.is.a.comment",
        "this.is.only.a.test",
        "    #    this.is.also a.comment    ",
    ];
    let infile = Cursor::new(names.join("\n").as_bytes());
    let expected = vec![
        "this.is.a.test",
        "this.is.only.a.test",
    ];
    let received = filter_koan_names(infile);
    let expected: Vec<String> = expected.iter().map(|s| s.to_string()).collect();
    assert_eq!(expected, received);
}

#[test]
fn test_all_blank_or_comment_lines_produce_empty_output() {
    let names = [" ", "# This is a comment.", "\t", "    # This is also a comment."];
    let infile = Cursor::new(names.join("\n").as_bytes());
    let expected: Vec<String> = vec![];
    let received = filter_koan_names(infile);
    assert_eq!(expected, received);
}

#[test]
fn test_empty_input_produces_empty_testsuite() {
    let names: Vec<String> = vec![];
    let suite = koans_suite(names.clone());
    assert!(suite.is_empty());
}

#[test]
fn test_testcase_names_appear_in_testsuite() {
    let names = [
        "koans.about_asserts.AboutAsserts",
        "koans.about_none.AboutNone",
        "koans.about_strings.AboutStrings",
    ];
    let suite = koans_suite(names.iter().map(|&s| s.to_string()).collect());
    let expected = vec!["AboutAsserts", "AboutNone", "AboutStrings"];
    let received: Vec<String> = suite.iter().map(|test| test.name.clone()).collect();
    let mut received_sorted: Vec<String> = received.iter().cloned().collect();
    received_sorted.sort();
    let mut expected_sorted: Vec<String> = expected.iter().map(|s| s.to_string()).collect();
    expected_sorted.sort();
    assert_eq!(expected_sorted, received_sorted);
}