use linkedin2username::GEO_REGIONS;

#[test]
fn test_geo_regions_us() {
    let geo = GEO_REGIONS.lock().unwrap();
    assert_eq!(geo.get("us").unwrap(), "103644278");
}

#[test]
fn test_geo_regions_all_have_str() {
    let geo = GEO_REGIONS.lock().unwrap();
    for (code, val) in geo.iter() {
        assert!(code.is_ascii() || !code.is_empty()); // code is always String
        assert!(val.is_ascii() || !val.is_empty());
        assert!(val.chars().all(|c| c.is_ascii_digit()), "All values must be numeric string");
    }
}