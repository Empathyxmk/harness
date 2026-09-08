use wjcryptlib::rc4output;

#[test]
fn test_no_arguments_rc4output() {
    let result = rc4output::run_command(&[]);
    assert!(result.is_err());
}

#[test]
fn test_key_only_rc4output() {
    let args = ["00112233AABBCCDD"];
    let result = rc4output::run_command(&args);
    assert!(result.is_ok());
}

#[test]
fn test_valid_minimal_rc4output() {
    let args = ["00112233AABBCCDD", "10"];
    let result = rc4output::run_command(&args);
    assert!(result.is_ok());
}

#[test]
fn test_valid_dropn_rc4output() {
    let args = ["00112233AABBCCDD", "10", "7"];
    let result = rc4output::run_command(&args);
    assert!(result.is_ok());
}