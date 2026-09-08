use aadhithya_rajiniPP::lexer::Lexer;
use aadhithya_rajiniPP::utils::read_yml;

#[test]
fn test_public_lexer_tokenization_for_identifier() {
    let tokens = read_yml("rajinipp/token.yml");
    let lexer = Lexer::new(&tokens);
    let result = lexer.lex("varX1 = 9");
    let token_names: Vec<&str> = result.iter().map(|t| t.name).collect();
    assert!(token_names.contains(&"ID"));
}

#[test]
fn test_public_lexer_ignores_comments() {
    let tokens = read_yml("rajinipp/token.yml");
    let lexer = Lexer::new(&tokens);
    let code = "num = 2  !! this is a comment\nprint num";
    let result = lexer.lex(code);
    let code_fragment: String = result.iter().map(|tok| tok.value).collect();
    assert!(!code_fragment.contains("!!"));
}

#[test]
#[should_panic(expected = "File not found")]
fn test_public_lexer_raise_file_exception() {
    // This purposely raises panic as in Python's FileNotFoundError
    let _ = aadhithya_rajiniPP::utils::read_yml("missing_token.yml");
}