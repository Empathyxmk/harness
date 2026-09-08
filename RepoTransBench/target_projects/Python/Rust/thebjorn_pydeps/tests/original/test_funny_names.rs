use crate::filemaker::TempFileTree;
use crate::simpledeps::simpledeps;
use std::collections::HashSet;

#[test]
fn test_from_html5lib() {
    let files = r#"
        foo:
            - __init__.py
            - a.py: |
                from bar import py
        bar:
            - __init__.py
            - py.py: |
                barpy = 42
    "#;
    let tmp = TempFileTree::from_yaml(files);
    let expected: HashSet<String> = ["bar -> foo.a", "bar.py -> foo.a"].iter().map(|s| s.to_string()).collect();
    assert_eq!(simpledeps("foo", "--show-deps -LINFO -vv"), expected);
}

#[test]
fn test_multidot() {
    let files = r#"
        foo.bar.py: |
            from math import pi
    "#;
    let tmp = TempFileTree::from_yaml(files);
    let expected: HashSet<String> = ["math -> foo.bar.py"].iter().map(|s| s.to_string()).collect();
    assert_eq!(simpledeps("foo.bar.py", "--show-deps --pylib -LINFO -vv"), expected);
}