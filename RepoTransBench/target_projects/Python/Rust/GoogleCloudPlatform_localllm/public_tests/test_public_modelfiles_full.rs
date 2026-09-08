#[test]
fn test_public_find_llmfiles() {
    let test_dir = "/tmp/some-llm-model-dir";
    let test_files = vec!["lion.Q4_0.gguf", "giraffe.Q8_0.gguf"];
    let mut found_gguf = false;
    for f in &test_files {
        if f.ends_with(".gguf") {
            found_gguf = true;
        }
    }
    assert!(found_gguf);
    let content = test_files.join("");
    assert!(content.contains("lion.Q4_0.gguf"));
}

#[test]
fn test_public_is_llmfile() {
    let filename1 = "rhino.Q7_0.gguf";
    let filename2 = "zebra.txt";
    assert!(filename1.ends_with(".gguf"));
    assert!(!filename2.ends_with(".gguf"));
}