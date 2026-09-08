use crate::filemaker::TempFileTree;
use crate::simpledeps::simpledeps;
use std::collections::HashSet;

#[test]
fn test_from_customlib_public() {
    let files = r#"
        zoo:
            - __init__.py
            - tiger.py: |
                from custom import py
        custom:
            - __init__.py
            - py.py: |
                somevar = 100
    "#;
    let tmp = TempFileTree::from_yaml(files);
    let expected: HashSet<String> = ["custom -> zoo.tiger", "custom.py -> zoo.tiger"].iter().map(|s| s.to_string()).collect();
    assert_eq!(simpledeps("zoo", "--show-deps -LINFO -vv"), expected);
}

#[test]
fn test_multidot_public() {
    let files = r#"
        alpha.beta.py: |
            from random import randint
    "#;
    let tmp = TempFileTree::from_yaml(files);
    let expected: HashSet<String> = ["random -> alpha.beta.py"].iter().map(|s| s.to_string()).collect();
    assert_eq!(simpledeps("alpha.beta.py", "--show-deps --pylib -LINFO -vv"), expected);
}