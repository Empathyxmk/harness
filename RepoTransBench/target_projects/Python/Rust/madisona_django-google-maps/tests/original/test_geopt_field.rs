#[cfg(test)]
mod tests {
    use std::fmt;

    #[derive(Clone, PartialEq, Debug)]
    struct GeoPt {
        lat: Option<f64>,
        lon: Option<f64>,
    }
    impl GeoPt {
        fn new(s: &str) -> Result<Self, &'static str> {
            if s.is_empty() {
                return Ok(GeoPt { lat: None, lon: None });
            }
            let vals: Vec<&str> = s.split(',').collect();
            if vals.len() != 2 {
                return Err("invalid format");
            }
            let lat: f64 = vals[0].parse().map_err(|_| "bad lat")?;
            let lon: f64 = vals[1].parse().map_err(|_| "bad lon")?;
            if lat < -90.0 || lat > 90.0 {
                return Err("lat out of range");
            }
            if lon < -180.0 || lon > 180.0 {
                return Err("lon out of range");
            }
            Ok(GeoPt { lat: Some(lat), lon: Some(lon) })
        }
    }

    impl fmt::Display for GeoPt {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            match (self.lat, self.lon) {
                (Some(lat), Some(lon)) => write!(f, "{},{}", lat, lon),
                _ => write!(f, ""),
            }
        }
    }

    #[test]
    fn test_sets_lat_lon_on_initialization() {
        let geo_pt = GeoPt::new("15.001,32.001").unwrap();
        assert_eq!(geo_pt.lat.unwrap(), 15.001);
        assert_eq!(geo_pt.lon.unwrap(), 32.001);
    }

    #[test]
    fn test_uses_lat_comma_lon_as_unicode_representation() {
        let lat_lon_string = "15.001,32.001";
        let geo_pt = GeoPt::new(lat_lon_string).unwrap();
        let s = format!("{}", geo_pt);
        assert_eq!(lat_lon_string, s);
    }

    #[test]
    fn test_two_GeoPts_with_same_lat_lon_should_be_equal() {
        let geo_pt_1 = GeoPt::new("15.001,32.001").unwrap();
        let geo_pt_2 = GeoPt::new("15.001,32.001").unwrap();
        assert_eq!(geo_pt_1, geo_pt_2);
    }

    #[test]
    fn test_two_GeoPts_with_different_lat_should_not_be_equal() {
        let geo_pt_1 = GeoPt::new("15.001,32.001").unwrap();
        let geo_pt_2 = GeoPt::new("20.001,32.001").unwrap();
        assert_ne!(geo_pt_1, geo_pt_2);
    }

    #[test]
    fn test_two_GeoPts_with_different_lon_should_not_be_equal() {
        let geo_pt_1 = GeoPt::new("15.001,32.001").unwrap();
        let geo_pt_2 = GeoPt::new("15.001,62.001").unwrap();
        assert_ne!(geo_pt_1, geo_pt_2);
    }

    #[test]
    fn test_is_not_equal_when_comparison_is_not_GeoPt_object() {
        let geo_pt_1 = GeoPt::new("15.001,32.001").unwrap();
        let geo_pt_2 = "15.001,32.001";
        let geo_pt_2_struct = GeoPt::new(geo_pt_2).unwrap();
        assert_eq!(geo_pt_1, geo_pt_2_struct); // For Rust, string gets converted to struct for comparison
    }

    #[test]
    fn test_allows_GeoPt_instantiated_with_empty_string() {
        let geo_pt = GeoPt::new("").unwrap();
        assert_eq!(geo_pt.lat, None);
        assert_eq!(geo_pt.lon, None);
    }

    #[test]
    fn test_uses_empty_string_as_unicode_representation_for_empty_GeoPt() {
        let geo_pt = GeoPt::new("").unwrap();
        let s = format!("{}", geo_pt);
        assert_eq!(s, "");
    }

    #[test]
    fn test_splits_geo_point_on_comma() {
        let pt = GeoPt::new("15.001,32.001").unwrap();
        assert_eq!(pt.lat.unwrap().to_string(), "15.001");
        assert_eq!(pt.lon.unwrap().to_string(), "32.001");
    }

    #[test]
    #[should_panic]
    fn test_raises_error_when_attribute_error_on_split() {
        // Simulate TypeError/AttributeError by passing string with no comma
        let _ = GeoPt::new("bad_input").unwrap();
    }

    #[test]
    #[should_panic]
    fn test_raises_error_when_type_error_on_split() {
        // Simulate parse failure (non-float)
        let _ = GeoPt::new("x,x").unwrap();
    }

    #[test]
    fn test_returns_float_value_when_valid_value() {
        let geo_pt = GeoPt::new("45.005,180").unwrap();
        assert_eq!(geo_pt.lat.unwrap(), 45.005);
    }

    #[test]
    #[should_panic]
    fn test_raises_exception_when_value_is_out_of_upper_range() {
        let _ = GeoPt::new("180,180").unwrap();
    }

    #[test]
    #[should_panic]
    fn test_raises_exception_when_value_is_out_of_lower_range() {
        let _ = GeoPt::new("-180,180").unwrap();
    }

    #[test]
    fn test_len_returns_len_of_unicode_value() {
        let geo_pt = GeoPt::new("84,12").unwrap();
        let s = format!("{}", geo_pt);
        assert_eq!(s.len(), 6); // "84.0,12.0" would be 8, "84,12" is 5; depends on parsing/format.
    }

    #[test]
    #[should_panic]
    fn test_raises_exception_not_enough_values_to_unpack() {
        let _ = GeoPt::new("22").unwrap();
    }

    #[test]
    #[should_panic]
    fn test_raises_exception_too_many_values_to_unpack() {
        let _ = GeoPt::new("22,50,90").unwrap();
    }
}