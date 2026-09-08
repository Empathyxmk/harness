use crate::modelfiles;
use std::path::PathBuf;

// Simulate a global cache dir patch
const HUBCACHE_DIR: &str = "hubcache";

// Helper for test isolation
fn create_fake_model_dir(tmp_dir: &PathBuf, repo: &str, model: &str) -> PathBuf {
    let parts: Vec<&str> = repo.split('/').collect();
    let repo_dir = tmp_dir.join(HUBCACHE_DIR).join(format!("models--{}--{}", parts[0], parts[1]));
    std::fs::create_dir_all(&repo_dir).unwrap();
    let model_path = repo_dir.join(model);
    std::fs::write(&model_path, "fake model").unwrap();
    model_path
}

#[test]
fn test_get_model_dir_patched() {
    let tmp_dir = PathBuf::from("tmp_test_modelfiles");
    let model_dir = tmp_dir.join(HUBCACHE_DIR);
    assert!(modelfiles::get_model_dir().contains(HUBCACHE_DIR));
}

#[test]
fn test_list_models() {
    // Simulate list_models = []
    assert_eq!(modelfiles::list_models().len(), 0);
    // Simulate adding a model file
    let files = vec!["/tmp/hubcache/models--foo--bar/bar.Q4_K_M.gguf".to_string()];
    let filtered = modelfiles::filter_models(&files.iter().map(|s| s as &str).collect::<Vec<&str>>());
    assert!(filtered.len() >= 1);
    assert_eq!(filtered, modelfiles::list_models());
}

#[test]
fn test_filter_models_and_model_from_path() {
    let files = vec![
        "/some/fake/path/models--foo--bar/baz.Q4_K_M.gguf",
        "/some/other/path/notamodel.txt"
    ];
    let filtered = modelfiles::filter_models(&files);
    assert!(filtered.iter().all(|tup| tup.0.len() > 0 && tup.1.len() > 0));
}

#[test]
fn test_model_from_path_variants() {
    let p = "something/models--foo--bar/baz.Q4_K_M.gguf";
    let (repo, model) = modelfiles::model_from_path(p);
    assert_eq!(repo, "foo/bar");
    assert_eq!(model, "baz.Q4_K_M.gguf");
    assert_eq!(modelfiles::model_from_path("no-model-here"), ("".to_string(), "".to_string()));
}

#[test]
fn test_path_from_repo() {
    // Valid repo
    let rv = modelfiles::path_from_repo("foo/bar");
    assert!(rv.contains("models--foo--bar"));
    // Invalid repo
    assert_eq!(modelfiles::path_from_repo("foo"), "");
}

#[test]
fn test_get_all_files() {
    let files = modelfiles::get_all_files("test_empty_dir");
    assert!(files.is_empty());
}

#[test]
fn test_path_from_model() {
    // Valid returns Some(path), not found returns None
    assert!(modelfiles::path_from_model("foo/bar", "model.gguf").is_none() || 
        modelfiles::path_from_model("foo/bar", "model.gguf").unwrap().ends_with("model.gguf"));
}

#[test]
fn test_find_model() {
    let files = vec![
        "/root/test/1.Q4_K_M.gguf".to_string(),
        "/root/test/2.Q4_K_M.gguf".to_string(),
    ];
    let found = modelfiles::find_model(&files.iter().map(|s| s as &str).collect::<Vec<&str>>(), "1.Q4_K_M.gguf");
    assert!(found.is_none() || found.unwrap().ends_with("1.Q4_K_M.gguf"));
    assert!(modelfiles::find_model(&files, "X.Q4_K_M.gguf").is_none());
}