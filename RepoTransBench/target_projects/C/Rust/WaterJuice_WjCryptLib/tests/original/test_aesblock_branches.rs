use wjcryptlib::aesblock;

#[test]
fn test_without_d_flag_prints_usage() {
    // Should print usage/help due to missing flag
    let args = [
        "00112233445566778899aabbccddeeff",
        "112233445566778899aabbccddeeff",
    ];
    let result = aesblock::run_command(&args);
    assert!(result.is_err(), "Should print usage without -D");
}

#[test]
fn test_with_invalid_key() {
    let args = [
        "-D",
        "0011",
        "112233445566778899aabbccddeeff",
    ];
    let result = aesblock::run_command(&args);
    assert!(result.is_err(), "Invalid short key should fail");
}

#[test]
fn test_with_one_argument_print_usage() {
    let args = [
        "00112233445566778899aabbccddeeff"
    ];
    let result = aesblock::run_command(&args);
    assert!(result.is_err(), "Should print usage with only one arg");
}

#[test]
fn test_correct_usage_and_different_block() {
    let args = [
        "-D",
        "00112233445566778899aabbccddeeff",
        "aabbccddeeff00112233445566778899"
    ];
    let result = aesblock::run_command(&args);
    assert!(result.is_ok(), "Should succeed with correct usage");
}

#[test]
fn test_with_bad_block() {
    let args = [
        "-D",
        "00112233445566778899aabbccddeeff",
        "badblock"
    ];
    let result = aesblock::run_command(&args);
    assert!(result.is_err(), "Non-hex block should fail");
}