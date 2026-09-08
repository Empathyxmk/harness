use rdflib_jsonld::*;

#[test]
fn test_version_defined() {
    assert_eq!(VERSION, "0.6.2");
    assert!(VERSION.is_ascii());
}

#[test]
fn test_author_defined() {
    assert!(AUTHOR.contains("RDFLib"));
    assert!(AUTHOR.is_ascii());
}

#[test]
fn test_contact_defined() {
    assert!(CONTACT.contains("@"));
    assert!(CONTACT.is_ascii());
}

#[test]
fn test_docformat_defined() {
    assert_eq!(DOCFORMAT, "restructuredtext");
}

#[test]
fn test_module_docstring_exists() {
    // Rust doc comments are not runtime-accessible as __doc__, but we can check the file doc comment
    let doc_content = include_str!("../../src/lib.rs");
    let doc = doc_content.trim().to_lowercase();
    assert!(doc.contains("plugin for rdflib") || doc.contains("a plugin for rdflib"));
}