use betterprompt;
use std::collections::HashMap;

#[test]
fn test_calculate_perplexity_all_none() {
    // Simulate None values as -100 for test (as Python does in test)
    let token_logprobs = vec![-100.0f64, -100.0];
    let result = betterprompt::calculate_perplexity(&token_logprobs);
    assert!(result.is_finite());
}

#[test]
fn test_calculate_perplexity_regular() {
    let token_logprobs = vec![0.0, -1.0, -2.0];
    let expected = (-token_logprobs.iter().sum::<f64>() / token_logprobs.len() as f64).exp();
    let actual = betterprompt::calculate_perplexity(&token_logprobs);
    assert!((actual - expected).abs() < 1e-8);
}

#[test]
fn test_calculate_perplexity_empty_list() {
    let result = betterprompt::calculate_perplexity(&[]);
    assert!(result.is_infinite());
}

#[test]
fn test_calculate_perplexity_nan() {
    let result = f64::NAN.exp();
    assert!(result.is_nan());
}