use crate::filemaker::TempFileTree;
use crate::simpledeps::simpledeps;

#[test]
fn test_file() {
    let files = r#"
        a.py: |
            import collections
    "#;
    let tmp = TempFileTree::from_yaml(files);
    // The test expects empty set because stdlib imports are ignored by default.
    assert_eq!(simpledeps("a.py", ""), std::collections::HashSet::<String>::new());
}

#[test]
fn test_file_in_sub_directory() {
    let files = r#"
        foo:
            - a:
                - b.py: |
                    import c
                - c.py: ""
    "#;
    let tmp = TempFileTree::from_yaml(files);
    // Should show 'c -> b.py' in the output
    assert!(simpledeps("foo/a/b.py", "").contains("c -> b.py"));
}

#[test]
fn test_file_in_directory() {
    let files = r#"
            - a:
                - b.py: |
                    import c
                - c.py: ""
    "#;
    let tmp = TempFileTree::from_yaml(files);
    assert!(simpledeps("a/b.py", "").contains("c -> b.py"));
}

#[test]
fn test_file_pylib() {
    let files = r#"
        a.py: |
            import collections
    "#;
    let tmp = TempFileTree::from_yaml(files);
    assert!(simpledeps("a.py", "--pylib").contains("collections -> a.py"));
}

#[test]
fn test_file_pyliball() {
    let files = r#"
        a.py: |
            import collections
    "#;
    let tmp = TempFileTree::from_yaml(files);
    assert!(simpledeps("a.py", "--pylib --pylib-all").contains("collections -> a.py"));
}