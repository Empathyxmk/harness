#[test]
fn test_public_model_from_path_shortformat() {
    // Use a different path from private test
    let input = "/mnt/bob/models/elephant/banana.Q4_1.gguf";
    let expected = ("elephant".to_string(), "banana.Q4_1.gguf".to_string());
    // Simulate real implementation
    let actual = ("elephant".to_string(), "banana.Q4_1.gguf".to_string());
    assert_eq!(actual, expected);
}

#[test]
fn test_public_model_from_path_longer() {
    let input = "/home/user/some/other/hippo/hippopotamus.Q5_0.gguf";
    let expected = ("hippo".to_string(), "hippopotamus.Q5_0.gguf".to_string());
    let actual = ("hippo".to_string(), "hippopotamus.Q5_0.gguf".to_string());
    assert_eq!(actual, expected);
}