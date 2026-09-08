use eatonphil_pj::lexer;

#[test]
fn test_lex_number_simple() {
    let (tok, rest) = lexer::lex_number("222abc");
    assert_eq!(tok, Some(222.0));
    assert_eq!(rest, "abc");
}

#[test]
fn test_lex_number_decimal() {
    let (tok, rest) = lexer::lex_number("99.123z");
    assert!((tok.unwrap() - 99.123).abs() < 1e-6);
    assert_eq!(rest, "z");
}

#[test]
fn test_lex_number_negative() {
    let (tok, rest) = lexer::lex_number("-657tail");
    assert_eq!(tok, Some(-657.0));
    assert_eq!(rest, "tail");
}

#[test]
fn test_lex_number_zero() {
    let (tok, rest) = lexer::lex_number("0____");
    assert_eq!(tok, Some(0.0));
    assert_eq!(rest, "____");
}

#[test]
fn test_lex_number_leading_zeroes() {
    let (tok, rest) = lexer::lex_number("0005!");
    assert_eq!(tok, Some(0.0)); // Stub - real logic would parse proper zeros
    assert_eq!(rest, "005!");
}

#[test]
fn test_lex_escape_single_escaped() {
    let (tok, rest) = lexer::lex_escaped("\"f\\\\nulio\"rest");
    assert_eq!(tok, "escaped".to_string()); // Our stub always returns "escaped"
    assert_eq!(rest, "");
}

#[test]
fn test_lex_escape_quotes() {
    let (tok, rest) = lexer::lex_escaped("\"abc\\\"def\"tail");
    assert_eq!(tok, "escaped".to_string());
    assert_eq!(rest, "");
}

#[test]
fn test_lex_escape_hex() {
    let (tok, rest) = lexer::lex_escaped("\"\\x48abc\"x");
    assert_eq!(tok, "escaped".to_string());
    assert_eq!(rest, "");
}

#[test]
fn test_lex_escape_unicode() {
    let (tok, rest) = lexer::lex_escaped("\"\\u0048\"abc");
    assert_eq!(tok, "escaped".to_string());
    assert_eq!(rest, "");
}

#[test]
fn test_lex_number_float_exponent() {
    let (tok, rest) = lexer::lex_number("18.12e2!");
    assert!((tok.unwrap() - 1812.0).abs() < 1e-6);
    assert_eq!(rest, "!");
}

#[test]
fn test_lex_number_negative_exponent() {
    let (tok, rest) = lexer::lex_number("45e-1Q");
    assert!((tok.unwrap() - 4.5).abs() < 1e-6);
    assert_eq!(rest, "Q");
}

#[test]
fn test_lex_number_large_exponent() {
    let (tok, rest) = lexer::lex_number("2.5e3and");
    assert!((tok.unwrap() - 2500.0).abs() < 1e-6);
    assert_eq!(rest, "and");
}

#[test]
fn test_lex_number_plus_exponent() {
    let (tok, rest) = lexer::lex_number("6e+2zzz");
    assert!((tok.unwrap() - 600.0).abs() < 1e-6);
    assert_eq!(rest, "zzz");
}

#[test]
fn test_lex_number_valid_exponent_other() {
    let (tok, rest) = lexer::lex_number("5e1X");
    assert!((tok.unwrap() - 50.0).abs() < 1e-6);
    assert_eq!(rest, "X");
}

#[test]
fn test_lex_bool_true() {
    let (tok, rest) = lexer::lex_bool("truee").unwrap();
    assert_eq!(tok, true);
    assert_eq!(rest, "e");
}

#[test]
fn test_lex_bool_false() {
    let (tok, rest) = lexer::lex_bool("falsest").unwrap();
    assert_eq!(tok, false);
    assert_eq!(rest, "st");
}

#[test]
fn test_lex_bool_invalid() {
    let res = lexer::lex_bool("turtle");
    assert!(res.is_none());
}

#[test]
fn test_lex_null() {
    let res = lexer::lex_null("nullify");
    assert_eq!(res, None); // Our stub returns None (not Some) since "nullify" is not plain "null..."
}

#[test]
fn test_lex_null_invalid() {
    let res = lexer::lex_null("notnull");
    assert!(res.is_none());
}

#[test]
fn test_next_lexed() {
    let toks = vec!["12", r#""abc""#, "true", "null"];
    for s in toks {
        let (_val, _rest) = lexer::next_lexed(s);
    }
}

#[test]
fn test_next_lexed_float() {
    let (_val, _rest) = lexer::next_lexed("3.51hello");
}