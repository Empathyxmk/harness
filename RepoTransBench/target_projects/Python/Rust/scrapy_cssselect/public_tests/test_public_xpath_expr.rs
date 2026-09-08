use scrapy_cssselect_rs::xpath::XPathExpr;

#[test]
fn test_xpath_expr_str_and_add_condition_public() {
    let mut x = XPathExpr::new("/root/", "span", "active=true");
    assert!(x.to_string().starts_with("/root/span[active="));
    x.add_condition("visible=false");
    assert!(x.condition.contains("visible=false"));
    assert!(x.condition.contains("active=true"));
}

#[test]
fn test_xpath_expr_add_name_test_public() {
    let mut x = XPathExpr::new("//", "section", "");
    x.add_name_test();
    assert_eq!(x.element, "*");
    assert!(x.condition.contains("name()"));
}

#[test]
fn test_xpath_expr_add_star_prefix_public() {
    let mut x = XPathExpr::new("/foo/", "*", "");
    x.add_star_prefix();
    assert!(x.path.starts_with("/foo/*"));
}

#[test]
fn test_xpath_expr_join_public() {
    let x1 = XPathExpr::new("/root/", "header", "data=val1");
    let x2 = XPathExpr::new("/sibling/", "footer", "data=val2");
    let r = x1.join("//", &x2, "-end-", true);
    assert!(r.element.starts_with("footer"));
    assert!(r.path.contains("//") || r.path.contains("-end-"));
}