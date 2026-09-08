#[test]
fn test_import_some_attrs_public() {
    // Choose different subset of attributes and their presence
    use scrapy_cssselect_rs as cssselect;
    let _ = cssselect::GenericTranslator;
    let _ = cssselect::parse;
    let _ = cssselect::SelectorError;
    let _ = cssselect::Selector;
    let _ = cssselect::HTMLTranslator;
    // Ensured type exists
}

#[test]
fn test_version_public() {
    use scrapy_cssselect_rs as cssselect;
    assert!(!cssselect::VERSION.is_empty());
    assert!(cssselect::__version__.is_ascii());
    assert!(cssselect::__version__.len() > 0);
}