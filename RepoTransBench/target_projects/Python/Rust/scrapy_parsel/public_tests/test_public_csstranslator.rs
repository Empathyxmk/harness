// Rust translation of public_tests/test_public_csstranslator.py

#[cfg(test)]
mod tests {
    use super::*;
    use crate::csstranslator::{GenericTranslator, HTMLTranslator, SelectorError};

    #[test]
    fn test_generic_translator_cache_behavior_public() {
        let g = GenericTranslator::new();
        assert_eq!(
            g.css_to_xpath("a#main.class").unwrap(),
            "//a[contains(concat(\" \",normalize-space(@class),\" \"),\" class \")][@id = \"main\"]"
        );
        assert_eq!(
            g.css_to_xpath("a#main.class").unwrap(),
            g.css_to_xpath("a#main.class").unwrap()
        );
    }

    #[test]
    fn test_htmltranslator_inheritance_public() {
        // In Rust, use traits or type check.
        // Example: ensure HTMLTranslator "is a" GenericTranslator.
        let h = HTMLTranslator::new();
        assert!(h.as_generic().is_some());
    }

    #[test]
    #[should_panic]
    fn test_xpath_expr_join_type_check_public() {
        let g = GenericTranslator::new();
        // joiner must be string, so passing something else should panic
        g.xpath_expr("span", Some(123)); // This should panic or return error.
    }

    #[test]
    fn test_xpath_pseudo_element_unknown_public() {
        let g = GenericTranslator::new();
        let err = g.css_to_xpath("a::unknown");
        assert!(matches!(err, Err(SelectorError(_))));
    }
}