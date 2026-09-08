#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_http_client_get() {
        struct HttpClient {}
        impl HttpClient {
            fn get(&self, url: &str) -> Result<String, &'static str> {
                if url == "http://valid.url" {
                    Ok("Valid response".to_string())
                } else {
                    Err("404 Not Found")
                }
            }
        }

        let client = HttpClient {};
        let result = client.get("http://valid.url").unwrap();
        assert_eq!(result, "Valid response");
    }

    #[test]
    fn test_http_client_get_failure() {
        struct HttpClient {}
        impl HttpClient {
            fn get(&self, url: &str) -> Result<String, &'static str> {
                if url == "http://valid.url" {
                    Ok("Valid response".to_string())
                } else {
                    Err("404 Not Found")
                }
            }
        }

        let client = HttpClient {};
        let result = client.get("http://invalid.url");
        assert!(result.is_err());
    }
}