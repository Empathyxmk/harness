use crate::filemaker::TempFileTree;
use crate::simpledeps::simpledeps;

#[test]
fn test_file_public() {
    let files = r#"
        b.py: |
            import math
    "#;
    let tmp = TempFileTree::from_yaml(files);
    assert_eq!(simpledeps("b.py", ""), std::collections::HashSet::<String>::new());
}

#[test]
fn test_file_in_sub_directory_public() {
    let files = r#"
        baz:
            - d:
                - e.py: |
                    import f
                - f.py: ""
    "#;
    let tmp = TempFileTree::from_yaml(files);
    assert!(simpledeps("baz/d/e.py", "").contains("f -> e.py"));
}

#[test]
fn test_file_in_directory_public() {
    let files = r#"
            - x:
                - y.py: |
                    import z
                - z.py: ""
    "#;
    let tmp = TempFileTree::from_yaml(files);
    assert!(simpledeps("x/y.py", "").contains("z -> y.py"));
}

#[test]
fn test_file_pylib_public() {
    let files = r#"
        q.py: |
            import sys
    "#;
    let tmp = TempFileTree::from_yaml(files);
    assert!(simpledeps("q.py", "--pylib").contains("sys -> q.py"));
}

#[test]
fn test_file_pyliball_public() {
    let files = r#"
        q.py: |
            import sys
    "#;
    let tmp = TempFileTree::from_yaml(files);
    assert!(simpledeps("q.py", "--pylib --pylib-all").contains("sys -> q.py"));
}