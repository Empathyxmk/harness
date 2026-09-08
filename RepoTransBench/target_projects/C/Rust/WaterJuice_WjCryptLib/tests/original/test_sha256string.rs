use wjcryptlib::sha256string;

#[test]
fn test_no_arguments_sha256string() {
    let result = sha256string::run_command(&[]);
    assert!(result.is_err());
}

#[test]
fn test_simple_arg_sha256string() {
    let hash = sha256string::calculate_hash("hello world");
    assert_eq!(
        hash,
        "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9",
        "SHA256 for 'hello world'"
    );
}