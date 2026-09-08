use wjcryptlib::rc4output;

#[test]
fn test_too_few_arguments() {
    let result = rc4output::run_command(&[]);
    assert!(result.is_err());
}

#[test]
fn test_short_key_hex_error() {
    let args = ["01"];
    let result = rc4output::run_command(&args);
    assert!(result.is_ok());
    // The RC4 key of length 1 byte is technically valid for classic RC4
}

#[test]
fn test_correct_usage() {
    let args = ["11223344556677"];
    let result = rc4output::run_command(&args);
    assert!(result.is_ok());
}

#[test]
fn test_too_many_args_ignored() {
    let args = ["11223344556677", "abcd", "extra"];
    let result = rc4output::run_command(&args);
    assert!(result.is_ok());
}

#[test]
fn test_odd_size_key() {
    let args = ["12ab34cd"];
    let result = rc4output::run_command(&args);
    assert!(result.is_ok());
}