use betterprompt::*;
use serial_test::serial;
use std::collections::HashMap;
use std::env;
use serde_json::json;

#[test]
#[serial]
fn test_public_get_from_dict_or_env_missing() {
    let key = "PUBLIC_ENV_KEY";
    env::remove_var(key);
    let dict: HashMap<String,String> = HashMap::new();
    let result = get_from_dict_or_env(key, Some(&dict));
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("PUBLIC_ENV_KEY"));
}

#[test]
#[serial]
fn test_public_get_from_dict_or_env_dict() {
    let key = "DICT_ONLY_KEY";
    let mut d = HashMap::new();
    d.insert(key.to_string(), "dict_value".to_string());
    env::set_var(key, "env_value");
    let result = get_from_dict_or_env(key, Some(&d));
    assert_eq!(result.unwrap(), "dict_value");
    env::remove_var(key);
}

#[test]
#[serial]
fn test_public_get_from_dict_or_env_env() {
    let key = "ENV_ONLY_KEY_PUBLIC";
    env::remove_var(key);
    env::set_var(key, "from_env_public");
    let result = get_from_dict_or_env(key, None);
    assert_eq!(result.unwrap(), "from_env_public");
    env::remove_var(key);
}

#[test]
fn test_public_openai_class_dummy() {
    let result = DummyOpenAICompletion::create();
    assert!(result.contains_key("choices"));
}

#[test]
fn test_public_call_openai_api_key() {
    let dummy_logprobs = vec![1.23, -0.8, 3.14];
    let custom = move |_args: &[&str], _kwargs: &HashMap<&str, String>| {
        serde_json::from_value(json!({
            "choices": [
                {"logprobs": { "token_logprobs": dummy_logprobs }}
            ]
        })).unwrap()
    };
    set_openai_handler(Box::new(custom));
    let result = call_openai("test prompt", None, Some("a_public_key"));
    assert_eq!(result, Some(vec![1.23, -0.8, 3.14]));
    reset_openai_handler();
}

#[test]
fn test_public_calculate_perplexity_all_negative() {
    let token_logprobs = vec![-2.0, -4.0, -6.0];
    let expected = (-token_logprobs.iter().sum::<f64>() / (token_logprobs.len() as f64)).exp();
    let actual = calculate_perplexity(&token_logprobs);
    assert!((actual - expected).abs() < 1e-8);
}

#[test]
fn test_public_calculate_perplexity_empty() {
    let result = calculate_perplexity(&[]);
    assert!(result.is_infinite());
}