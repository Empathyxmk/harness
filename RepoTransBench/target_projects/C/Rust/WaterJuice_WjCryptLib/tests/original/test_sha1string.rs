use wjcryptlib::sha1string;

#[test]
fn test_no_arguments_sha1string() {
    let result = sha1string::run_command(&[]);
    assert!(result.is_err());
}

#[test]
fn test_simple_arg_sha1string() {
    let hash = sha1string::calculate_hash("hello world");
    assert_eq!(
        hash,
        "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed",
        "SHA1 for 'hello world'"
    );
}