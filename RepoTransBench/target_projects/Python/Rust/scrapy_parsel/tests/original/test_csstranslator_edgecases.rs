// Rust translation of tests/test_csstranslator_edgecases.py

#[cfg(test)]
mod tests {
    use super::*;
    use crate::csstranslator::{GenericTranslator, HTMLTranslator, XPathExpr};

    #[test]
    fn test_xpathexpr_str_textnode_and_attribute() {
        let mut e = XPathExpr::from_xpath(XPathExpr::new("*"));
        e.textnode = true;
        let s = e.to_string();
        assert!(s.ends_with("text()"));
        let mut e = XPathExpr::from_xpath(XPathExpr::new("*"));
        e.attribute = Some("class".to_string());
        let s = e.to_string();
        assert!(s.ends_with("@class"));
        let mut e = XPathExpr::from_xpath(XPathExpr::new("*"));
        e.textnode = true;
        e.attribute = Some("href".to_string());
        let s = e.to_string();
        assert!(s.contains("text()") || s.contains("@href"));
    }

    // ... other tests for error handling, etc ...

}