use betterprompt::*;

#[test]
fn test_public_calculate_perplexity_all_zeroes() {
    let token_logprobs = vec![0.0, 0.0, 0.0];
    let result = calculate_perplexity(&token_logprobs);
    assert!((result - 1.0).abs() < 1e-8);
}

#[test]
fn test_public_calculate_perplexity_positive_and_negative() {
    let token_logprobs = vec![1.0, -1.0, -2.0, 2.0];
    let expected = (-token_logprobs.iter().sum::<f64>() / (token_logprobs.len() as f64)).exp();
    let actual = calculate_perplexity(&token_logprobs);
    assert!((actual - expected).abs() < 1e-8);
}

#[test]
fn test_public_calculate_perplexity_empty_list() {
    let result = calculate_perplexity(&[]);
    assert!(result.is_infinite());
}

#[test]
fn test_public_calculate_perplexity_large() {
    let token_logprobs = vec![10.0, 12.0, 15.0];
    let expected = (-token_logprobs.iter().sum::<f64>() / (token_logprobs.len() as f64)).exp();
    let actual = calculate_perplexity(&token_logprobs);
    assert!((actual - expected).abs() < 1e-8);
}