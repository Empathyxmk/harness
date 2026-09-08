// Public: Translated from public_tests/public_deye_timeofuse_service_test.py

#[test]
fn test_timeofuse_public_offpeak() {
    assert_eq!(pick_timeofuse_public(2), "offpeak");
}
fn pick_timeofuse_public(hour: u32) -> &'static str {
    if hour < 6 { "offpeak" } else { "peak" }
}