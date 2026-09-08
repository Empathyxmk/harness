#[cfg(test)]
mod public_tests {
    use super::*;
    use us_states::*;

    #[test]
    fn test_public_fips_lookup() {
        assert_eq!(lookup("48", Field::FIPS).unwrap(), *TX);
    }
    
    #[test]
    fn test_public_abbr_lookup() {
        assert_eq!(lookup("CO", Field::Abbr).unwrap(), *CO);
    }

    #[test]
    fn test_public_name_lookup() {
        assert_eq!(lookup("Florida", Field::Name).unwrap(), *FL);
    }    
}