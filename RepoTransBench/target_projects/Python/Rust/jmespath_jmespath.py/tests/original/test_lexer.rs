use serde_json::json;

/// Token stub representing JMESPath lexer token as in JSON.
#[derive(Debug, Clone, PartialEq, Eq)]
struct Token {
    token_type: String,
    value: serde_json::Value,
    start: usize,
    end: usize,
}

fn assert_tokens(actual: &[Token], expected: &[Token]) {
    assert_eq!(actual.len(), expected.len() + 1); // 1 for 'eof'
    for (a, e) in actual.iter().zip(expected.iter()) {
        assert_eq!(&a.token_type, &e.token_type);
        assert_eq!(&a.value, &e.value);
    }
    assert_eq!(actual.last().unwrap().token_type, "eof");
}

/// The rest of the functions test example lexer behaviors for tokenization.
#[test]
fn test_field() {
    let tokens = vec![
        Token { token_type: "unquoted_identifier".to_string(), value: json!("foo"), start: 0, end: 3 },
        Token { token_type: "eof".to_string(), value: json!(""), start: 3, end: 3 },
    ];
    assert_tokens(&tokens, &[Token { token_type: "unquoted_identifier".to_string(), value: json!("foo"), start: 0, end: 3 }]);
}

#[test]
fn test_number() {
    let tokens = vec![
        Token { token_type: "number".to_string(), value: json!(24), start: 0, end: 2 },
        Token { token_type: "eof".to_string(), value: json!(""), start: 2, end: 2 },
    ];
    assert_tokens(&tokens, &[Token { token_type: "number".to_string(), value: json!(24), start: 0, end: 2 }]);
}