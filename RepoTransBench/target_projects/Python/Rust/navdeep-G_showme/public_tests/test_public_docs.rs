//! Port of public_tests/test_public_docs.py to Rust

use showme::MODULE_DOC;

#[test]
fn test_public_docs() {
    // Slightly different docstring test: check for "showme" or "core" in the docstring
    let doc = MODULE_DOC;
    assert!(doc.to_lowercase().contains("showme") || doc.to_lowercase().contains("core"));
}