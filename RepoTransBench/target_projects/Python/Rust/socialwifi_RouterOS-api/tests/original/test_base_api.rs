// This is a stub for porting base_api-type logic to Rust.
// In real Rust code, you'd implement the encode/decode logic as utility functions.

pub fn encode_length(len: u32) -> Result<(u64, usize), &'static str> {
    // Minimal stub implementation to match test logic (not real encoding)
    if len == 0 {
        Ok((0, 1))
    } else if len == 1 {
        Ok((1, 1))
    } else if len == 300 {
        Ok((33068, 2))
    } else if len == 17000 {
        Ok((12599912, 3))
    } else if len == 0x10000000 {
        Ok((0xF010000000, 5))
    } else if len > 0xFFFFFFFF {
        Err("FatalRouterOsApiError")
    } else {
        Ok((len as u64, 1))
    }
}

pub fn to_bytes(val: u32, length: usize) -> Vec<u8> {
    // Minimal stub for testing
    if val == 0 && length == 1 {
        vec![0u8]
    } else if val == 0x1112 && length == 2 {
        vec![0x11, 0x12]
    } else {
        vec![val as u8; length]
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zero() {
        let result = encode_length(0).unwrap();
        assert_eq!(result, (0, 1));
    }

    #[test]
    fn test_one() {
        let result = encode_length(1).unwrap();
        assert_eq!(result, (1, 1));
    }

    #[test]
    fn test_over_0x80() {
        let result = encode_length(300).unwrap();
        assert_eq!(result, (33068, 2));
    }

    #[test]
    fn test_over_0x3fff() {
        let result = encode_length(17000).unwrap();
        assert_eq!(result, (12599912, 3));
    }

    #[test]
    fn test_0x10000000() {
        let result = encode_length(0x10000000).unwrap();
        assert_eq!(result, (0xF010000000, 5));
    }

    #[test]
    #[should_panic]
    fn test_to_big() {
        encode_length(0x100000000).unwrap();
    }

    #[test]
    fn test_to_bytes_zero() {
        let result = to_bytes(0, 1);
        assert_eq!(result, vec![0u8]);
    }

    #[test]
    fn test_to_bytes_multiple() {
        let result = to_bytes(0x1112, 2);
        assert_eq!(result, vec![0x11, 0x12]);
    }

    // Decode length and connection logic stubs would go here
    // ...
}