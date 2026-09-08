use crate::filemaker::TempFileTree;
use crate::simpledeps::{depgrf, DummyDepGraph};
use serde_json::Value;

#[test]
fn test_dep2dot() {
    let files = r#"
        foo:
            - __init__.py
            - a.py: |
                from . import b
            - b.py
    "#;
    let tmp = TempFileTree::from_yaml(files);
    let g = depgrf("foo");
    // The depgrf output should be valid json containing certain keys.
    let d: Value = serde_json::from_str(&format!("{}", g)).unwrap();
    assert!(d["foo"]["imported_by"].to_string().contains("__main__"));
}