use crate::filemaker::TempFileTree;
use crate::simpledeps::{depgrf, DummyDepGraph};
use serde_json::Value;

#[test]
fn test_dep2dot_public() {
    let files = r#"
        bar:
            - __init__.py
            - x.py: |
                from . import y
            - y.py
    "#;
    let tmp = TempFileTree::from_yaml(files);
    let g = depgrf("bar");
    let d: Value = serde_json::from_str(&format!("{}", g)).unwrap();
    assert!(d["bar"]["imported_by"].to_string().contains("__main__"));
}