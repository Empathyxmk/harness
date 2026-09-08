use dsprenkels_randombytes::{randombytes, set_mock_random_filler, RandomFiller};

/// Coverage oriented basic test: normal usage
#[test]
fn test_randombytes_basic() {
    let mut buf = [0u8; 32];
    let ret = randombytes(&mut buf).unwrap_or(-1);
    // Should succeed and buffer should not be all-zeros
    assert_eq!(ret, ());
    assert!(buf.iter().any(|&b| b != 0), "Buffer should not be all zeros");
}

/// Edge case: zero-length buffer
#[test]
fn test_randombytes_zero_length() {
    let mut buf: [u8; 0] = [];
    let ret = randombytes(&mut buf).unwrap_or(-1);
    assert_eq!(ret, (), "Zero-length buffer should succeed");
}

/// Stress test: large buffer (not too big for CI/environment)
#[test]
fn test_randombytes_large() {
    let mut buf = [0u8; 1024];
    let ret = randombytes(&mut buf).unwrap_or(-1);
    // Don't check content, just that it works
    assert_eq!(ret, (), "Large buffer should succeed");
}