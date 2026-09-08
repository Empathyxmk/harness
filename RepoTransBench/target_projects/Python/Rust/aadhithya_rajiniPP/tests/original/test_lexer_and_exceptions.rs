use aadhithya_rajiniPP::{lexer::Lexer, exceptions};

#[test]
fn test_lexer_add_and_get_tokens() {
    // Just a couple for smoke test
    let tokens = [("NUM", "\\d+"), ("PLUS", "\\+")];
    let lexer = Lexer::new(&tokens);
    let lex_obj = lexer.get_lexer();
    let result = lex_obj.lex("3 + 5");
    let names: std::collections::HashSet<_> = result.iter().map(|t| t.name).collect();
    assert!(names.contains("NUM"));
    assert!(names.contains("PLUS"));
}

#[test]
fn test_lexer_ignore_comments_and_whitespace() {
    let tokens = [("ID", "[a-zA-Z_]+"), ("EQ", "=")];
    let lexer = Lexer::new(&tokens);
    let lex_obj = lexer.get_lexer();
    let code = "foo = bar   !! this is a comment\nbaz=qux";
    let result = lex_obj.lex(code);
    let names: Vec<_> = result.iter().map(|t| t.name).collect();
    assert_eq!(names, ["ID", "EQ", "ID", "ID", "EQ", "ID"]);
}

#[test]
fn test_break_exception() {
    let err = exceptions::BreakException("Break now!");
    let msg = format!("{}", err);
    assert!(msg.contains("BreakException"));
}

#[test]
fn test_return_exception_value() {
    let msg = "Return!";
    let ret_val = 42;
    let err = exceptions::ReturnException(msg, ret_val);
    let msg_display = format!("{}", err);
    assert!(msg_display.contains("ReturnException"));
    assert!(msg_display.contains(msg));
}