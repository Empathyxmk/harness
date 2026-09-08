#[cfg(test)]
mod test_public_wikipedia_object {
    use super::*;

    #[test]
    fn test_public_wikipedia_init_different_language() {
        let wiki = Wikipedia::new("public-test/3.0".to_string(), "fr".to_string());
        assert!(wiki.is_some());
        let wiki = wiki.unwrap();
        assert_eq!(wiki.language, "fr");
        assert_eq!(wiki.extract_format, ExtractFormat::WIKI);
    }

    #[test]
    fn test_public_wikipedia_init_all_args_different() {
        let wiki = Wikipedia::new_with_all(
            "public-test/4.0".to_string(),
            "es".to_string(),
            Some("an".to_string()),
            ExtractFormat::WIKI,
            Some(std::collections::HashMap::from([("Test".to_string(), "Header".to_string())])),
            Some(std::collections::HashMap::from([("foo".to_string(), "bar".to_string())])),
            2,
        );
        assert_eq!(wiki.language, "es");
        assert_eq!(wiki.variant, Some("an".to_string()));
        assert_eq!(wiki.extract_format, ExtractFormat::WIKI);
    }

    #[test]
    #[should_panic]
    fn test_public_wikipedia_init_short_useragent_raises() {
        let _ = Wikipedia::new("ai".to_string(), "fr".to_string());
    }
}