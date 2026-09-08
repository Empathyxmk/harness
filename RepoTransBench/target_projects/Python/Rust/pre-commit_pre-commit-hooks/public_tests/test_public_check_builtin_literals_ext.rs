// Rust translation of public check_builtin_literals test

#[test]
fn test_check_file_other_types() {
    let dir = tempfile::TempDir::new().unwrap();
    let file_path = dir.path().join("other_types.py");
    let code = r#"
x = dict()
y = set()
z = bool()
p = float()
q = int()
r = tuple()
s = str()
"#;
    std::fs::write(&file_path, code).unwrap();
    let res = check_builtin_literals_check_file(file_path.to_str().unwrap());
    let types_reported: std::collections::HashSet<_> = res.iter().map(|c| c.name.clone()).collect();
    let exp: std::collections::HashSet<&str> = [
        "dict", "set", "bool", "float", "int", "tuple", "str"
    ].iter().cloned().collect();
    assert_eq!(types_reported, exp);
}

#[test]
fn test_check_file_with_other_ignore() {
    let dir = tempfile::TempDir::new().unwrap();
    let file_path = dir.path().join("ignore_other_types.py");
    let code = r#"
x = set()
y = bool()
z = float()
"#;
    std::fs::write(&file_path, code).unwrap();
    let res = check_builtin_literals_check_file_with_ignore(file_path.to_str().unwrap(), vec!["set", "float"]);
    let types_reported: Vec<_> = res.iter().map(|c| c.name.clone()).collect();
    assert!(types_reported.contains(&"bool".to_string()));
    assert!(!types_reported.contains(&"set".to_string()));
    assert!(!types_reported.contains(&"float".to_string()));
}

// Stub implementation
fn check_builtin_literals_check_file(_path: &str) -> Vec<Call> { vec![] }
fn check_builtin_literals_check_file_with_ignore(_path: &str, _ignore: Vec<&str>) -> Vec<Call> { vec![] }

#[derive(Debug, Clone, PartialEq, Eq)]
struct Call {
    name: String,
}