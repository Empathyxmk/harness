use crate::modelfiles;

#[test]
fn test_filter_models() {
    let files = vec![
        "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/.no_exist/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/tokenizer.model",
        "/home/user/.cache/huggingface/hub/models--TheBloke--openinstruct-mistral-7B-GGUF/snapshots/0eda7ce8a5951a2839c32f0bf074eb21dd28ecd8/openinstruct-mistral-7b.Q4_K_M.gguf",
        "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/config.json",
        "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/refs/main",
        "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/snapshots/b5c676eb555d1e44b5381969c7901d31add6673d/smartyplats-7b-v2.Q4_K_M.gguf",
    ];
    let m = modelfiles::filter_models(&files.iter().map(|s| s as &str).collect::<Vec<&str>>());
    assert_eq!(m.len(), 2);
    assert_eq!(m[0].0, "TheBloke/openinstruct-mistral-7B-GGUF");
    assert_eq!(m[0].1, "openinstruct-mistral-7b.Q4_K_M.gguf");
    assert_eq!(m[1].0, "TheBloke/smartyplats-7B-v2-GGUF");
    assert_eq!(m[1].1, "smartyplats-7b-v2.Q4_K_M.gguf");
}

#[test]
fn test_model_from_path() {
    let (repo, model) = modelfiles::model_from_path(
        "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/llama-2-13b-ensemble-v5.Q4_K_M.gguf");
    assert_eq!(repo, "TheBloke/Llama-2-13B-Ensemble-v5-GGUF");
    assert_eq!(model, "llama-2-13b-ensemble-v5.Q4_K_M.gguf");
}

#[test]
fn test_model_from_path_unknown_format() {
    let (repo, model) = modelfiles::model_from_path("foo");
    assert_eq!(repo, "");
    assert_eq!(model, "");
}

#[test]
fn test_path_from_repo() {
    let repo_id = "TheBloke/Llama-2-13B-Ensemble-v5-GGUF";
    let path = modelfiles::path_from_repo(repo_id);
    assert!(path.ends_with(".cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF"));
}

#[test]
fn test_path_from_repo_unknown_format() {
    let path = modelfiles::path_from_repo("SomeRepo");
    assert_eq!(path, "");
}

#[test]
fn test_find_model() {
    let files = vec![
        "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/llama-2-13b-ensemble-v5.Q4_K_M.gguf",
        "/home/user/.cache/huggingface/hub/models--TheBloke--openinstruct-mistral-7B-GGUF/snapshots/0eda7ce8a5951a2839c32f0bf074eb21dd28ecd8/openinstruct-mistral-7b.Q4_K_M.gguf",
        "/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/config.json",
        "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/refs/main",
        "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/snapshots/b5c676eb555d1e44b5381969c7901d31add6673d/smartyplats-7b-v2.Q4_K_M.gguf",
    ];
    let model = "smartyplats-7b-v2.Q4_K_M.gguf";
    let path = modelfiles::find_model(&files.iter().map(|s| s as &str).collect::<Vec<&str>>(), model);
    assert!(path.is_none() || path.unwrap() == "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/snapshots/b5c676eb555d1e44b5381969c7901d31add6673d/smartyplats-7b-v2.Q4_K_M.gguf");
}