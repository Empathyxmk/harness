#[cfg(test)]
mod public_extra {
    use super::*;
    use us_states::*;

    #[test]
    fn test_state_name_and_abbr() {
        assert_eq!(CA.name, "California");
        assert_eq!(NY.abbr, "NY");
    }

    #[test]
    fn test_state_alternate() {
        assert_eq!(NY.fips, "36");
        assert_eq!(NV.capital, "Carson City");
    }    
}