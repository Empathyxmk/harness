use std::collections::HashMap;
use claude_to_chatgpt::adapter::{ClaudeAdapter, role_map, stop_reason_map};
use serde_json::{json, Map, Value};

#[test]
fn test_get_api_key_from_headers_public() {
    let ca = ClaudeAdapter::new("http://another-url");
    let mut headers = HashMap::new();
    headers.insert("authorization".to_string(), "Bearer another-key".to_string());
    assert_eq!(ca.get_api_key(&headers), "another-key");
    let mut ca = ClaudeAdapter::new("http://another-url");
    ca.claude_api_key = "second-env-key".to_string();
    let empty: HashMap<String, String> = HashMap::new();
    assert_eq!(ca.get_api_key(&empty), "second-env-key");
}

#[test]
fn test_convert_messages_to_prompt_roles_public() {
    let ca = ClaudeAdapter::new("public_url");
    let messages = vec![
        HashMap::from([("role", "user"), ("content", "How are you?")]),
        HashMap::from([("role", "assistant"), ("content", "I'm fine, thank you.")]),
        HashMap::from([("role", "system"), ("content", "System message here")])
    ];
    let prompt = ca.convert_messages_to_prompt(&messages);

    assert!(prompt.contains("\n\nHuman: How are you?"));
    assert!(prompt.contains("\n\nAssistant: I'm fine, thank you."));
    assert!(prompt.contains("\n\nHuman: How are you?"));
    assert!(prompt.trim_end().ends_with("Assistant:"));
}

#[test]
fn test_openai_to_claude_params_all_public() {
    let ca = ClaudeAdapter::default();
    let oai = json!({
        "model": "gpt-4-0314",
        "messages": [],
        "max_tokens": 1024,
        "stop": ["STOP_NOW"],
        "temperature": 0.55,
        "stream": false
    });
    let mut map = ca.openai_to_claude_params(&oai);
    assert_eq!(map["model"], json!("claude-v1"));
    assert_eq!(map["prompt"], json!("PROMPT!"));
    assert_eq!(map["max_tokens_to_sample"], json!(1024));
    assert_eq!(map["stop_sequences"], json!(["STOP_NOW"]));
    assert_eq!(map["temperature"], json!(0.55));
    assert_eq!(map["stream"], json!(false));
}

#[test]
fn test_openai_to_claude_params_partial_public() {
    let ca = ClaudeAdapter::default();
    let oai = json!({
        "model": "absent-model",
        "messages": []
    });
    let map = ca.openai_to_claude_params(&oai);
    assert_eq!(map["model"], json!("claude-2"));
    assert_eq!(map["prompt"], json!("PROMPT!"));
    assert_eq!(map["max_tokens_to_sample"], json!(100000));
}

#[test]
fn test_claude_to_chatgpt_response_stream_public() {
    let ca = ClaudeAdapter::default();
    let mut resp = Map::new();
    resp.insert("completion".into(), Value::String("Different completion".into()));
    resp.insert("stop_reason".into(), Value::String("max_tokens".into()));
    let response = ca.claude_to_chatgpt_response_stream(&resp);
    assert_eq!(response["choices"][0]["delta"]["content"], Value::String("Different completion".to_string()));
    assert_eq!(response["choices"][0]["finish_reason"], Value::String(stop_reason_map.get("max_tokens").unwrap().to_string()));
    assert_eq!(response["usage"]["completion_tokens"], Value::from(20));
}

#[test]
fn test_claude_to_chatgpt_response_no_stop_public() {
    let ca = ClaudeAdapter::default();
    let mut resp = Map::new();
    resp.insert("completion".into(), Value::String("A different completion text".into()));
    let response = ca.claude_to_chatgpt_response(&resp);
    assert_eq!(response["choices"][0]["message"]["content"], Value::String("A different completion text".to_string()));
    assert!(response["choices"][0]["finish_reason"].is_null());
    assert_eq!(response["usage"]["completion_tokens"], Value::from(25));
}

#[test]
fn test_convert_messages_to_prompt_correct_format_public() {
    let ca = ClaudeAdapter::default();
    let messages = vec![HashMap::from([("role", "user"), ("content", "What's up?")])];
    let result = ca.convert_messages_to_prompt(&messages);
    assert!(result.starts_with("\n\nHuman: What's up?") && result.ends_with("Assistant:"));
}