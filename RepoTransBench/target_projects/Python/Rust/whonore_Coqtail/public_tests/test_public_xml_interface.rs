use std::collections::HashMap;
use coqtail::xml_interface_public::*;

#[test]
fn test_public_escape_xml_symbol() {
    let result = escape("apples & bananas < oranges > \"g\"");
    assert!(result.contains("&amp;"));
    assert!(result.contains("&lt;"));
    assert!(result.contains("&gt;"));
    assert!(result.contains("&quot;"));
}

#[test]
fn test_public_unescape_xml_symbol() {
    let s = "&amp;hello&gt;&lt;test&gt;&quot;x&quot;";
    let result = unescape(s);
    assert!(result.contains("&"));
    assert!(result.contains(">"));
    assert!(result.contains("<"));
    assert!(result.contains("\""));
}

#[test]
fn test_public_make_elem_with_attrs() {
    let mut attrs = HashMap::new();
    attrs.insert("ripe", "yes");
    attrs.insert("color", "yellow");
    let elem = elem("fruit", "banana & apple", Some(&attrs));
    assert!(elem.contains("fruit"));
    assert!(elem.contains("ripe"));
    assert!(elem.contains("&amp;"));
}