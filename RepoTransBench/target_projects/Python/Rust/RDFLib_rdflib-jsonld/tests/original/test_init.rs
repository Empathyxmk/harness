// There is no import failure in Rust, but we can check all constants are accessible
use rdflib_jsonld::*;

#[test]
fn test_import_rdflib_jsonld() {
    // All symbols from lib.rs must be available
    let _: &str = VERSION;
    let _: &str = AUTHOR;
    let _: &str = CONTACT;
    let _: &str = DOCFORMAT;
    // Doc is checked by doc-test
    assert!(true);
}