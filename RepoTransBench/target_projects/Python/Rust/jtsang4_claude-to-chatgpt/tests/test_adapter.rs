use std::collections::HashMap;
use claude_to_chatgpt::adapter::{ClaudeAdapter, role_map, stop_reason_map};
use serde_json::{json, Map, Value};

#[test]
fn test_get_api_key_from_headers() {
    let ca = ClaudeAdapter::new("http://test-url");
    let mut headers = HashMap::new();
    headers.insert("authorization".to_string(), "Bearer secret-key".to_string());
    assert_eq!(ca.get_api_key(&headers), "secret-key");

    let mut ca = ClaudeAdapter::new("http://test-url");
    ca.claude_api_key = "backup-from-env".to_string();
    let empty: HashMap<String, String> = HashMap::new();
    assert_eq!(ca.get_api_key(&empty), "backup-from-env");
}

#[test]
fn test_convert_messages_to_prompt_roles() {
    let ca = ClaudeAdapter::new("url");
    let messages = vec![
        HashMap::from([("role", "user"), ("content", "hello")]),
        HashMap::from([("role", "assistant"), ("content", "hi!")]),
        HashMap::from([("role", "system"), ("content", "sysmsg")])
    ];
    let prompt = ca.convert_messages_to_prompt(&messages);
    assert!(prompt.contains("\n\nHuman: hello"));
    assert!(prompt.contains("\n\nAssistant: hi!"));
    assert!(prompt.contains("\n\nHuman: hello")); // both 'user' and 'system' -> 'Human'
    assert!(prompt.trim_end().ends_with("Assistant:"));
}

#[test]
fn test_openai_to_claude_params_all() {
    let ca = ClaudeAdapter::default();
    let oai = json!({
        "model": "gpt-3.5-turbo-0613",
        "messages": [],
        "max_tokens": 512,
        "stop": ["THE END"],
        "temperature": 0.3,
        "stream": true
    });
    let mut map = ca.openai_to_claude_params(&oai);
    assert_eq!(map["model"], json!("claude-2"));
    assert_eq!(map["prompt"], json!("PROMPT!"));
    assert_eq!(map["max_tokens_to_sample"], json!(512));
    assert_eq!(map["stop_sequences"], json!(["THE END"]));
    assert_eq!(map["temperature"], json!(0.3));
    assert_eq!(map["stream"], json!(true));
}

#[test]
fn test_openai_to_claude_params_partial() {
    let ca = ClaudeAdapter::default();
    let oai = json!({
        "model": "non-existent",
        "messages": []
    });
    let map = ca.openai_to_claude_params(&oai);
    assert_eq!(map["model"], json!("claude-2"));
    assert_eq!(map["prompt"], json!("PROMPT!"));
    assert_eq!(map["max_tokens_to_sample"], json!(100000));
}

#[test]
fn test_claude_to_chatgpt_response_stream() {
    let ca = ClaudeAdapter::default();
    let mut resp = Map::new();
    resp.insert("completion".into(), Value::String("Some completion text".into()));
    resp.insert("stop_reason".into(), Value::String("stop_sequence".into()));
    let response = ca.claude_to_chatgpt_response_stream(&resp);

    assert_eq!(
        response["choices"][0]["delta"]["content"],
        Value::String("Some completion text".to_string())
    );
    assert_eq!(
        response["choices"][0]["finish_reason"],
        Value::String(stop_reason_map.get("stop_sequence").unwrap().to_string())
    );
    assert_eq!(
        response["usage"]["completion_tokens"],
        Value::from(20) // stub: length of string
    );
}

#[test]
fn test_claude_to_chatgpt_response_no_stop() {
    let ca = ClaudeAdapter::default();
    let mut resp = Map::new();
    resp.insert("completion".into(), Value::String("Some completion text".into()));
    let response = ca.claude_to_chatgpt_response(&resp);

    assert_eq!(
        response["choices"][0]["message"]["content"],
        Value::String("Some completion text".to_string())
    );
    assert!(response["choices"][0]["finish_reason"].is_null());
    assert_eq!(response["usage"]["completion_tokens"], Value::from(20)); // stub length
}

#[test]
fn test_convert_messages_to_prompt_correct_format() {
    let ca = ClaudeAdapter::default();
    let messages = vec![HashMap::from([("role", "user"), ("content", "hi")])];
    let result = ca.convert_messages_to_prompt(&messages);
    assert!(result.starts_with("\n\nHuman: hi") && result.ends_with("Assistant:"));
}