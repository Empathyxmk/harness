#[test]
fn test_import_all_attrs() {
    // Check that relevant "public" API attributes exist
    use scrapy_cssselect_rs as cssselect;
    let attrs = [
        "ExpressionError",
        "FunctionalPseudoElement",
        "GenericTranslator",
        "HTMLTranslator",
        "Selector",
        "SelectorError",
        "SelectorSyntaxError",
        "parse",
    ];
    // Checking using Rust: exist as types or functions in the module. We'll test via compile (known good).
    let _ = cssselect::ExpressionError;
    let _ = cssselect::GenericTranslator;
    let _ = cssselect::HTMLTranslator;
    let _ = cssselect::SelectorSyntaxError;
    let _ = cssselect::SelectorError;
    let _ = cssselect::FunctionalPseudoElement;
    let _ = cssselect::parse;
    // No assert: type system guarantees these are there
}

#[test]
fn test_version() {
    use scrapy_cssselect_rs as cssselect;
    assert!(cssselect::VERSION.len() > 0);
    assert_eq!(cssselect::VERSION, cssselect::__version__);
}