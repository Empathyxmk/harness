#[cfg(test)]
mod tests {
    use super::*;
    use us_states::*;

    #[test]
    fn test_attribute() {
        for state in STATES.iter() {
            let state2 = lookup(state.abbr, Field::Abbr).unwrap();
            assert_eq!(state.abbr, state2.abbr);
            assert_eq!(state.fips, state2.fips);
        }
    }

    #[test]
    fn test_valid_timezones() {
        for state in STATES.iter() {
            if let Some(capital_tz) = &state.capital_tz {
                assert!(timezone::get_timezone(capital_tz).is_ok());
            }
        }
    }

    #[test]
    fn test_fips() {
        assert_eq!(lookup("24", Field::FIPS).unwrap().abbr, "MD");
    }
    
    #[test]
    fn test_name() {
        assert_eq!(lookup("Maryland", Field::Name).unwrap().abbr, "MD");
    }

    #[test]
    fn test_jellyfish_metaphone() {
        for state in STATES.iter() {
            assert_eq!(state.name_metaphone, jellyfish::metaphone(&state.name));
        }
    }
}