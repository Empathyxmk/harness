use crate::modeldownload;

#[test]
fn test_default_filename() {
    let repo_id = "TheBloke/Llama-2-13B-Ensemble-v5-GGUF";
    let filename = modeldownload::default_filename(repo_id);
    assert_eq!("llama-2-13b-ensemble-v5.Q4_K_M.gguf", filename);
}

#[test]
fn test_default_filename_unknown_format() {
    let filename = modeldownload::default_filename("foo");
    assert_eq!("", filename);
}

#[test]
fn test_default_filename_unsupported_ext() {
    let repo_id = "TheBloke/openinstruct-mistral-7B-GPTQ";
    let filename = modeldownload::default_filename(repo_id);
    assert_eq!("", filename);
}