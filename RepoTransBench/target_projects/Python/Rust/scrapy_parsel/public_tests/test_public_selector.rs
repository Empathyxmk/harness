// Rust translation of public_tests/test_public_selector.py

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parsel::Selector;

    #[test]
    fn test_extract_from_html() {
        let html = "<html><body><span>world</span></body></html>";
        let sel = Selector::from_html(html);
        assert_eq!(sel.xpath("//span/text()").get().unwrap(), "world");
    }

    #[test]
    fn test_css_selection() {
        let html = "<div><b>BoldContent</b></div>";
        let sel = Selector::from_html(html);
        assert_eq!(sel.css("b::text").get().unwrap(), "BoldContent");
    }

    #[test]
    fn test_extract_first_custom_default() {
        let html = "<root></root>";
        let sel = Selector::from_html(html);
        assert_eq!(sel.xpath("//missing/text()").get_or("nothing"), "nothing");
    }

    #[test]
    fn test_extract_list() {
        let html = "<ul><li>egg</li><li>cheese</li></ul>";
        let sel = Selector::from_html(html);
        let result = sel.css("li::text").getall();
        assert_eq!(result, vec!["egg", "cheese"]);
    }

    #[test]
    #[should_panic]
    fn test_error_handling_wrong_type() {
        // This will panic because Selector expects a string, not an object.
        Selector::from_html_object();
    }
}