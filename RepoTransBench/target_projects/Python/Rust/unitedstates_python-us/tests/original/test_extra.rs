#[cfg(test)]
mod tests {
    use super::*;
    use us_states::*;
    
    #[test]
    fn test_state_repr_and_str() {
        let s = State::new("Alabama", "AL", Some("01"));

        assert_eq!(format!("{:?}", s), format!("<State:{}>", s.name));
        assert_eq!(format!("{}", s), s.name);
    }

    #[test]
    fn test_shapefile_urls_with_fips() {
        let s = State::new("Alabama", "AL", Some("01"));
        let urls = s.shapefile_urls();
        assert!(urls.is_some());
        let urls = urls.unwrap();

        assert!(urls.contains_key("tract"));
        assert!(urls.contains_key("county"));
    }

    #[test]
    fn test_shapefile_urls_without_fips() {
        // Create a State with no FIPS
        let fake_state = State::new("Fake", "ZZ", None);
        assert!(fake_state.shapefile_urls().is_none());
    }

    #[test]
    fn test_lookup_with_field_argument() {
        let md = State::new("Maryland", "MD", Some("24"));
        assert_eq!(lookup("MD", Field::Abbr), Some(md.clone()));
        assert_eq!(lookup("24", Field::FIPS), Some(md.clone()));
    }

    #[test]
    fn test_lookup_no_match_returns_none() {
        assert!(lookup("nonesuchstate", Field::None).is_none());
    }

    #[test]
    fn test_mapping_default_and_custom() {
        let md_fips = mapping("abbr", "fips");
        assert_eq!(md_fips.get(&"MD"), Some(&"24".to_string()));
    }
}