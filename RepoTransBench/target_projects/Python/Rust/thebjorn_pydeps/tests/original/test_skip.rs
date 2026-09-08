use crate::filemaker::TempFileTree;
use crate::simpledeps::simpledeps;
use std::collections::HashSet;

#[test]
fn test_no_skip() {
    let files = r#"
        relimp:
            - __init__.py
            - a.py: |
                from . import b
            - b.py: |
                from . import c
            - c.py
    "#;
    let tmp = TempFileTree::from_yaml(files);
    let expected: HashSet<String> = ["relimp.b -> relimp.a", "relimp.c -> relimp.b"]
        .iter().map(|s| s.to_string()).collect();
    assert_eq!(simpledeps("relimp", ""), expected);
}