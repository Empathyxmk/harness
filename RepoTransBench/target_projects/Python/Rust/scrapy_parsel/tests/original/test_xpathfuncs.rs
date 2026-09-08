// Rust translation of tests/test_xpathfuncs.py

#[cfg(test)]
mod tests {
    use super::*;
    use crate::parsel::Selector;
    use crate::xpathfuncs::{set_xpathfunc};

    #[test]
    fn test_has_class_simple() {
        let body = r#"
        <p class="foo bar-baz">First</p>
        <p class="foo">Second</p>
        <p class="bar">Third</p>
        <p>Fourth</p>
        "#;
        let sel = Selector::from_html(body);
        assert_eq!(sel.xpath(r#"//p[has-class("foo")]/text()"#).getall(), vec!["First", "Second"]);
        assert_eq!(sel.xpath(r#"//p[has-class("bar")]/text()"#).getall(), vec!["Third"]);
        assert_eq!(sel.xpath(r#"//p[has-class("foo","bar")]/text()"#).getall(), Vec::<String>::new());
        assert_eq!(sel.xpath(r#"//p[has-class("foo","bar-baz")]/text()"#).getall(), vec!["First"]);
    }

    // ... continue with other tests translating error handling, etc.
}