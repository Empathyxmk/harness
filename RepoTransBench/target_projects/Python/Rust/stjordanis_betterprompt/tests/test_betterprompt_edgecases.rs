use betterprompt::*;
use serial_test::serial;
use std::collections::HashMap;
use std::env;

#[test]
#[serial]
fn test_get_from_dict_or_env_empty_dict_no_env() {
    let key = "TEST_MISSING_KEY";
    // Remove env var (if it exists)
    env::remove_var(key);
    let dict: HashMap<String, String> = HashMap::new();
    let result = get_from_dict_or_env(key, Some(&dict));
    assert!(result.is_err());
    assert!(result.unwrap_err().contains(key));
}

#[test]
#[serial]
fn test_get_from_dict_or_env_none_dict_env() {
    let key = "ENV_ONLY_KEY";
    env::set_var(key, "val");
    let result = get_from_dict_or_env(key, None);
    assert_eq!(result.unwrap(), "val");
    env::remove_var(key);
}

#[test]
#[serial]
fn test_get_from_dict_or_env_dict_empty() {
    let key = "NO_DICT_KEY";
    env::set_var(key, "from_env");
    let dict: HashMap<String, String> = HashMap::new();
    let result = get_from_dict_or_env(key, Some(&dict));
    assert_eq!(result.unwrap(), "from_env");
    env::remove_var(key);
}

#[test]
fn test_openai_class_and_dummy() {
    let val = DummyOpenAICompletion::create();
    assert!(val.contains_key("choices"));
}

#[test]
#[serial]
fn test_call_openai_api_key() {
    // Custom dummy handler
    use serde_json::json;
    let dummy_logprobs = vec![0.4, 0.5, 0.6];
    let custom = move |_args: &[&str], _kwargs: &HashMap<&str, String>| {
        serde_json::from_value(json!({
            "choices": [
                {"logprobs": { "token_logprobs": dummy_logprobs }}
            ]
        })).unwrap()
    };
    set_openai_handler(Box::new(custom));
    let result = call_openai("prompt", None, Some("explicit_key"));
    assert_eq!(result, Some(vec![0.4, 0.5, 0.6]));
    reset_openai_handler();
}

#[test]
fn test_calculate_perplexity_regular() {
    let token_logprobs = vec![0.0, -1.0, -2.0];
    let expected = (-token_logprobs.iter().sum::<f64>() / (token_logprobs.len() as f64)).exp();
    let actual = calculate_perplexity(&token_logprobs);
    assert!((actual - expected).abs() < 1e-8);
}

#[test]
fn test_calculate_perplexity_empty() {
    let result = calculate_perplexity(&[]);
    assert!(result.is_infinite());
}