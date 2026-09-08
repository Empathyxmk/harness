use crate::export::runit::*;

#[test]
fn test_get_service_name_public() {
    assert_eq!(get_service_name("xyapp", "cache", 2), "xyapp-cache-2");
    assert_eq!(get_service_name("dragon", "fire", 1), "dragon-fire-1");
}
#[test]
fn test_get_log_service_name_public() {
    assert_eq!(get_log_service_name("xyapp", "cache", 2), "xyapp-cache-2-log");
    assert_eq!(get_log_service_name("lion", "roar", 3), "lion-roar-3-log");
}