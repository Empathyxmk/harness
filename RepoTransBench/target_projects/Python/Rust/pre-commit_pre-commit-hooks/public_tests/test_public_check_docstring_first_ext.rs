#[test]
fn test_public_with_module_docstring_and_func() {
    let dir = tempfile::TempDir::new().unwrap();
    let file = dir.path().join("documented.py");
    let code = r#"
"""A top-level docstring."""

def foo():
    """Function docstring."""
    return True
"#;
    std::fs::write(&file, code).unwrap();
    assert_eq!(check_docstring_first_main(&[file.to_str().unwrap()]), 0);
}

#[test]
fn test_public_docstring_after_import() {
    let dir = tempfile::TempDir::new().unwrap();
    let file = dir.path().join("import_first.py");
    let code = r#"
import os

"""Wrong place for docstring."""
def bar():
    pass
"#;
    std::fs::write(&file, code).unwrap();
    assert_eq!(check_docstring_first_main(&[file.to_str().unwrap()]), 1);
}

#[test]
fn test_public_no_docstring() {
    let dir = tempfile::TempDir::new().unwrap();
    let file = dir.path().join("empty.py");
    let code = r#"
def hi():
    return "no docstring"
"#;
    std::fs::write(&file, code).unwrap();
    assert_eq!(check_docstring_first_main(&[file.to_str().unwrap()]), 1);
}

fn check_docstring_first_main(_args: &[&str]) -> i32 { 0 }