use serde_json::json;
use std::collections::HashMap;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_request_object() {
        let mut params = HashMap::new();
        params.insert("method".to_string(), json!("add_public"));
        params.insert("params".to_string(), json!([56, 34]));
        params.insert("_id".to_string(), json!(101));
        let request = JSONRPC10Request::new(params);  // Assuming constructor
        assert_eq!(request.unwrap().data()["method"], json!("add_public"));
    }

    // Translate all public tests fully
}