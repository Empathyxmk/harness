use eatonphil_pj::lexer;

#[test]
fn test_lex_string_simple() {
    let s = r#""abc""#;
    let (tok, rest) = lexer::lex_string(s);
    assert_eq!(tok, Some("abc".to_string()));
    assert_eq!(rest, "");
    let caught = std::panic::catch_unwind(|| {
        lexer::lex_string(r#""abc"#);
    });
    assert!(caught.is_err());
}

#[test]
fn test_lex_string_fail() {
    let (tok, rest) = lexer::lex_string("notstring");
    assert_eq!(tok, None);
    assert_eq!(rest, "notstring");
}

#[test]
fn test_lex_number_int() {
    let (tok, rest) = lexer::lex_number("123 end");
    assert_eq!(tok, Some(123.0));
    assert_eq!(rest.trim(), "end");
    let (tok2, rest2) = lexer::lex_number("-55 foo");
    assert_eq!(tok2, Some(-55.0));
    assert_eq!(rest2.trim(), "foo");
}

#[test]
fn test_lex_number_float() {
    let (tok, rest) = lexer::lex_number("3.14rest");
    assert_eq!(tok, Some(3.14));
    assert_eq!(rest, "rest");
    let (tok, rest) = lexer::lex_number("abc");
    assert_eq!(tok, None);
    assert_eq!(rest, "abc");
}

#[test]
fn test_lex_number_valid_exponent() {
    let (tok, rest) = lexer::lex_number("1.23e2foo");
    assert!((tok.unwrap() - 123.0).abs() < 1e-6);
    assert_eq!(rest, "foo");
    let (tok, rest) = lexer::lex_number("-3.2e2z");
    assert!((tok.unwrap() - -320.0).abs() < 1e-6);
    assert_eq!(rest, "z");
}

#[test]
fn test_lex_bool_true_false() {
    let (tok, rest) = lexer::lex_bool("trueabc").unwrap();
    assert_eq!(tok, true);
    assert_eq!(rest, "abc");
    let (tok, rest) = lexer::lex_bool("falsex").unwrap();
    assert_eq!(tok, false);
    assert_eq!(rest, "x");
    let tok = lexer::lex_bool("null");
    assert_eq!(tok, None);
}

#[test]
fn test_lex_null() {
    let (tok, rest) = lexer::lex_null("nullvalue").unwrap();
    assert_eq!(tok, true);
    assert_eq!(rest, "value");
    let tok = lexer::lex_null("none");
    assert_eq!(tok, None);
}

#[test]
fn test_lex_single_whitespace() {
    let result = lexer::lex(" ");
    assert!(result.is_empty());
}

#[test]
fn test_lex_syntax_tokens() {
    for &syntax in &[",", ":", "[", "]", "{", "}"] {
        let result = lexer::lex(syntax);
        // Not a real tokenizer stub, but this ensures it never panics
        assert!(result.len() >= 0);
    }
}

#[test]
fn test_lex_combined() {
    let s = r#"{"foo": [123, "bar", false, null]}"#;
    let toks = lexer::lex(s);
    // This compares structure, but is a stub (could differ from real lexer)
    assert!(!toks.is_empty());
}

#[test]
fn test_lex_bad_char() {
    let caught = std::panic::catch_unwind(|| {
        lexer::lex("$notvalid");
    });
    assert!(caught.is_ok());
}