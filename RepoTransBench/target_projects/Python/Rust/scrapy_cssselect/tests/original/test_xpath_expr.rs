use scrapy_cssselect_rs::xpath::XPathExpr;

#[test]
fn test_xpath_expr_str_and_add_condition() {
    let mut x = XPathExpr::new("//", "div", "foo=1");
    assert_eq!(x.to_string(), "//div[foo=1]");
    x.add_condition("bar=2");
    // Check that unbalanced parens are not present and bar=2 got added
    assert!(!x.condition.contains("[foo=1)"));
    assert!(x.condition.contains("bar=2"));
}

#[test]
fn test_xpath_expr_add_name_test() {
    let mut x = XPathExpr::new("//", "div", "");
    x.add_name_test();
    assert_eq!(x.element, "*");
    assert!(x.condition.contains("name()"));
}

#[test]
fn test_xpath_expr_add_star_prefix() {
    let mut x = XPathExpr::new("//", "*", "");
    x.add_star_prefix();
    assert!(
        x.path == "//*"
            || x.path.ends_with("*/")
            || x.path.ends_with('*')
    );
}

#[test]
fn test_xpath_expr_join() {
    let x1 = XPathExpr::new("//", "a", "foo=1");
    let x2 = XPathExpr::new("/*/", "span", "bar=2");
    let r = x1.join("|", &x2, "::", true);
    // Type and content checks
    assert!(r.element.starts_with("span"));
    assert!(r.path.contains("|") || r.path.contains("::"));
}