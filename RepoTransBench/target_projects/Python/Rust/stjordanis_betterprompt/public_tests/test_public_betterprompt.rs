use betterprompt::*;
use serial_test::serial;
use std::collections::HashMap;
use serde_json::json;
use std::env;

#[test]
fn test_public_call_openai_custom_model() {
    let dummy_logprobs = vec![-0.1, 2.5, -4.3];
    let custom = move |_args: &[&str], kwargs: &HashMap<&str, String>| {
        assert_eq!(kwargs.get("model").unwrap(), "public-model");
        serde_json::from_value(json!({
            "choices": [
                {"logprobs": { "token_logprobs": dummy_logprobs }}
            ]
        })).unwrap()
    };
    set_openai_handler(Box::new(custom));
    let res = call_openai("sample prompt here", Some("public-model"), Some("anypublickey")).unwrap();
    assert_eq!(res, vec![-0.1, 2.5, -4.3]);
    reset_openai_handler();
}

#[test]
#[serial]
fn test_public_call_openai_env() {
    let dummy_logprobs = vec![7.0, 8.0];
    let custom = move |_args: &[&str], _kwargs: &HashMap<&str, String>| {
        serde_json::from_value(json!({
            "choices": [
                {"logprobs": { "token_logprobs": dummy_logprobs }}
            ]
        })).unwrap()
    };
    set_openai_handler(Box::new(custom));
    env::set_var("OPENAI_API_KEY", "public_env_key_test");
    let res = call_openai("prompt string", None, None).unwrap();
    assert_eq!(res, vec![7.0, 8.0]);
    env::remove_var("OPENAI_API_KEY");
    reset_openai_handler();
}

#[test]
fn test_public_calculate_perplexity_different() {
    let token_logprobs = vec![-1.0, 0.0, 1.0, 2.0];
    let expected = (-token_logprobs.iter().sum::<f64>() / (token_logprobs.len() as f64)).exp();
    let actual = calculate_perplexity(&token_logprobs);
    assert!((actual - expected).abs() < 1e-8);
}