use homu_rust::utils;

#[test]
fn test_alphanumeric_only_public() {
    assert_eq!(utils::alphanumeric_only("xyz789GH@#!"), "xyz789GH");
    assert_eq!(utils::alphanumeric_only(" **&$  321 "), "321");
}