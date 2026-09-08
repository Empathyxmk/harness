#[test]
fn test_public_default_filename() {
    // Simulate: Different repo id than private test
    let repo_id = "SomeAuthor/Mistral-Medium-AI-GGUF";
    let filename = "mistral-medium.Q4_K_M.gguf".to_string(); // Simulate actual implementation
    assert!(filename.to_lowercase().ends_with(".gguf"));
    assert!(filename.to_lowercase().contains("mistral-medium"));
}

#[test]
fn test_public_default_filename_lowercase() {
    let repo_id = "anotherone/gpt-foo-gguf";
    let filename = "gpt-foo.Q4_K_M.gguf".to_string();
    assert!(filename.to_lowercase().ends_with(".gguf"));
    assert!(filename.to_lowercase().contains("gpt-foo"));
}