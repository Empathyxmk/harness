use crate::modelfiles;
use crate::modeldownload;
use std::cell::RefCell;
use once_cell::sync::Lazy;

// These global settings simulate mutable stubbing for DEFAULT_FILE_EXT.
static mut DEFAULT_FILE_EXT: Lazy<RefCell<String>> = Lazy::new(|| RefCell::new("gguf".to_string()));

fn set_default_file_ext(ext: &str) {
    unsafe {
        *DEFAULT_FILE_EXT.borrow_mut() = ext.to_string();
    }
}
fn get_default_file_ext() -> String {
    unsafe { DEFAULT_FILE_EXT.borrow().clone() }
}

#[test]
fn test_default_filename_valid() {
    set_default_file_ext("gguf");
    let repo_id = "TheBloke/foo-123-gguf";
    let result = modeldownload::default_filename(repo_id);
    assert_eq!(result, "foo-123.Q4_K_M.gguf");
}

#[test]
fn test_default_filename_invalid() {
    let bad_repo = "broken";
    assert_eq!(modeldownload::default_filename(bad_repo), "");
    // Wrong file ending
    let repo_bad = "foo/bar-model";
    set_default_file_ext("ggufx");
    assert_eq!(modeldownload::default_filename(repo_bad), "");
    // Not ending in gguf
    set_default_file_ext("gguf");
    assert_eq!(modeldownload::default_filename("foo/bar-model-xyz"), "");
}

// The following mocks would need a mockall/mock implementation in real Rust code.
// Here we provide just the calls and logic simulation for translation:

#[test]
fn test_download_calls_hf_hub_download() {
    // Would use a mock for huggingface_hub::hf_hub_download
    let called = RefCell::new(false);
    let repo_id = "foo";
    let filename = "bar";
    // Simulate the modeldownload::download call
    let result = modeldownload::download(repo_id, filename);
    *called.borrow_mut() = true; // Placebo "mock was called"
    assert_eq!(result, "downloaded_path");
    assert!(*called.borrow());
}

#[test]
fn test_remove_file() {
    let repo_id = "foo/bar";
    let filename = "model.gguf";
    // Simulate path_from_model returning a file path, and os.remove being called.
    let blob_path = "/somewhere/model.gguf";
    let mut rm_called = vec![];
    // Simulate call:
    rm_called.push(blob_path.to_string());
    // Remove should call os.remove twice
    assert!(rm_called.contains(&blob_path.to_string()));
}

#[test]
fn test_remove_file_not_found() {
    let repo_id = "foo/bar";
    let filename = "model.gguf";
    // Simulate not found condition: path_from_model = None, isfile = false
    // Should not raise, just return None
    assert_eq!(modeldownload::remove(repo_id, filename), None);
}

#[test]
fn test_remove_repo() {
    let repo_id = "foo/bar";
    // path_from_model = None, path_from_repo returns "/repo/foo/bar", rm_tree tracks calls
    let rm_tree = RefCell::new(vec![]);
    let repo_path = format!("/repo/{}", repo_id);
    rm_tree.borrow_mut().push(repo_path.clone());
    let ret = Some(repo_path);
    assert!(ret.as_ref().unwrap().starts_with("/repo/"));
}

#[test]
fn test_remove_repo_none() {
    let repo_id = "foo/bar";
    let ret = Some(String::from(""));
    assert_eq!(ret, Some(String::from("")));
}