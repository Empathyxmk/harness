#[cfg(test)]
mod tests {
    use super::*;
    use reqwest::StatusCode;

    #[tokio::test]
    async fn test_public_caa_api_calls() {
        let url = "http://example.com/api/caa";
        let response = reqwest::get(url).await.unwrap();

        assert_eq!(response.status(), StatusCode::OK);
        
        let response_text = response.text().await.unwrap();
        assert!(response_text.contains("CAA API Response"));
    }
}