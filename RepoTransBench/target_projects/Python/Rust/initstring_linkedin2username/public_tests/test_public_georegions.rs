use linkedin2username::GEO_REGIONS;

#[test]
fn test_public_geo_regions_us() {
    let geo = GEO_REGIONS.lock().unwrap();
    assert_eq!(geo.get("us").unwrap(), "103644278");
}

#[test]
fn test_public_geo_regions_all_have_str() {
    let geo = GEO_REGIONS.lock().unwrap();
    for (region, val) in geo.iter() {
        assert!(region.is_ascii() || !region.is_empty());
    }
}