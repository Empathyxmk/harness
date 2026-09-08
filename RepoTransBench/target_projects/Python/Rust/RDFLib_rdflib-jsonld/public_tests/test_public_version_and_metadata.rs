use std::fs;
use std::path::Path;
use rdflib_jsonld::*;

#[test]
fn test_module_has_version() {
    // VERSION const must exist and be valid: contains at least one '.' and is a string
    assert!(VERSION.contains('.'));
    assert!(VERSION.chars().all(|c| c.is_ascii_graphic() || c == '.'));
}

#[test]
fn test_module_author_and_contact() {
    // AUTHOR and CONTACT must exist and be strings, CONTACT must look like an email
    assert!(!AUTHOR.is_empty());
    assert!(CONTACT.contains('@') && CONTACT.contains('.'));
}

#[test]
fn test_setup_py_has_import_or_class() {
    let setup_py = Path::new("setup.py");
    assert!(setup_py.exists(), "setup.py not found");
    let contents = fs::read_to_string(setup_py).expect("Failed to read setup.py");
    let lowered = contents.to_lowercase();
    assert!(lowered.contains("import") || lowered.contains("class"), "No 'import' or 'class' keyword found in setup.py");
}

#[test]
fn test_module_docstring_mentions_jsonld() {
    // Rust doc comments: check for docstring at top of lib.rs
    let doc_content = fs::read_to_string("src/lib.rs").expect("Could not read src/lib.rs");
    let doc_lower = doc_content.to_lowercase();
    assert!(doc_lower.contains("jsonld") || doc_lower.contains("json-ld"),
        "lib.rs docstring should mention jsonld or json-ld");
}