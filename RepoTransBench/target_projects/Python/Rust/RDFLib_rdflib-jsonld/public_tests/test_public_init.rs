use rdflib_jsonld::*;

#[test]
fn test_import_rdflib_jsonld_public() {
    let docstr = include_str!("../src/lib.rs");
    assert!(docstr.trim().is_empty() || docstr.starts_with("//!") || docstr.starts_with("#!")); // Would be string or none
    assert!(VERSION.is_ascii());
    assert!(AUTHOR.is_ascii());
    assert!(CONTACT.is_ascii());
    assert!(DOCFORMAT.is_ascii());
}