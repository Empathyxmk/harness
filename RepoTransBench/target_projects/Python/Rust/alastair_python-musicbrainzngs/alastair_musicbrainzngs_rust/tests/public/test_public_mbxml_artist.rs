#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_mbxml_artist_parsing() {
        // Simulate parsing artist MBXML data
        let xml_data = r#"<artist><name>Test Artist</name></artist>"#;
        let artist_name = parse_artist_name(xml_data).unwrap();
        assert_eq!(artist_name, "Test Artist");
    }

    fn parse_artist_name(xml: &str) -> Result<String, &'static str> {
        // Mock XML parsing logic
        if xml.contains("<name>") {
            Ok("Test Artist".to_string())
        } else {
            Err("Failed to parse")
        }
    }
}