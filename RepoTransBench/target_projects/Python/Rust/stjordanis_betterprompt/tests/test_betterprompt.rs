use betterprompt::*;
use serial_test::serial;
use std::collections::HashMap;

#[test]
fn test_metadata() {
    assert!(betterprompt::VERSION.is_ascii());
    assert!(betterprompt::AUTHOR.is_ascii());
    assert!(betterprompt::COPYRIGHT.is_ascii());
    assert!(betterprompt::LICENSE.is_ascii());

    // __all__ list must include get_from_dict_or_env
    assert!(betterprompt::ALL.iter().any(|&x| x == "get_from_dict_or_env"));
}

#[test]
fn test_dummy_openai_completion_create() {
    let result = DummyOpenAICompletion::create();
    assert!(result.contains_key("choices"));
}

#[test]
#[serial]
fn test_openai_completion_static() {
    use serde_json::json;
    // Save original handler & override
    let custom = |_args: &[&str], _kwargs: &HashMap<&str, String>| {
        serde_json::from_value(json!({
            "choices": [
                {"logprobs": { "token_logprobs": [0.5] }}
            ]
        })).unwrap()
    };
    set_openai_handler(Box::new(custom));
    let out = call_openai("prompt", None, None).unwrap();
    assert_eq!(out, vec![0.5]);
    reset_openai_handler();
}