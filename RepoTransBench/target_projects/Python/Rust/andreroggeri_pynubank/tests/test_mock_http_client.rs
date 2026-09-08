#[cfg(test)]
mod tests {
    #[test]
    fn test_mock_http_response() {
        // Imagine we are simulating an HTTP client response here
        struct MockHttpResponse {
            status_code: u16,
            body: String,
        }

        let response = MockHttpResponse {
            status_code: 200,
            body: String::from("OK"),
        };

        assert_eq!(response.status_code, 200);
        assert_eq!(response.body, "OK");
    }
}