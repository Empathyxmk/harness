use wjcryptlib::md5string;

#[test]
fn test_no_arguments_md5string() {
    // Simulates running with no argument, expecting error
    let result = md5string::run_command(&[]);
    assert!(result.is_err());
}

#[test]
fn test_simple_arg_md5string() {
    let hash = md5string::calculate_hash("test123");
    assert_eq!(
        hash,
        "cc03e747a6afbbcbf8be7668acfebee5",
        "MD5 for 'test123'"
    );
}