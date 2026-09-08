use jsonrpc::utils::{JSONSerializable, DatetimeDecimalEncoder, is_invalid_params};
use std::time::SystemTime;
use serde_json::json;
use std::collections::HashMap;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_json_serializable() {
        struct A;

        impl JSONSerializable for A {
            fn to_json(&self) -> serde_json::Value {
                json!({"test": "value"})
            }
        }

        let a = A;
        assert_eq!(a.to_json(), json!({"test": "value"}));
    }

    #[test]
    fn test_datetime_decimal_encoder() {
        let encoder = DatetimeDecimalEncoder;
        let date = SystemTime::now();
        let serialized = encoder.encode(date);  // Simulate encoding
        assert!(serialized.is_ok());
    }

    #[test]
    fn test_is_invalid_params() {
        assert!(is_invalid_params(|x: i32, y: i32| x + y, 1));  // Too few args
    }

    // Continue with all tests from test_utils.py
}