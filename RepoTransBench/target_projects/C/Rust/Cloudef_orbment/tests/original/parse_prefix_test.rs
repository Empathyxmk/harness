// Translated from tests/parse_prefix_test.c

fn parse_prefix(input: Option<&str>, output: &mut [u8]) -> i32 {
    match input {
        None => return -1,
        Some(s) => {
            if output.len() == 0 {
                return -1;
            }
            let bytes = s.as_bytes();
            if bytes.len() + 1 > output.len() {
                return -2;
            }
            output[..bytes.len()].copy_from_slice(bytes);
            // Null terminate
            if bytes.len() < output.len() {
                output[bytes.len()] = 0;
            }
            0
        }
    }
}

#[test]
fn test_parse_prefix_basic() {
    let mut output = [0u8; 16];
    let ret = parse_prefix(Some("abc"), &mut output);
    assert_eq!(ret, 0);
    let result = std::ffi::CStr::from_bytes_until_nul(&output).unwrap();
    assert_eq!(result.to_str().unwrap(), "abc");
}

#[test]
fn test_parse_prefix_null_input() {
    let mut output = [0u8; 16];
    let ret = parse_prefix(None, &mut output);
    assert_eq!(ret, -1);
}

#[test]
fn test_parse_prefix_null_output() {
    // Since Rust slices can't be null, simulate with len zero
    let ret = parse_prefix(Some("abc"), &mut []);
    assert_eq!(ret, -1);
}

#[test]
fn test_parse_prefix_overflow() {
    let mut output = [0u8; 2];
    let ret = parse_prefix(Some("abc"), &mut output);
    assert_eq!(ret, -2);
}