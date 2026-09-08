use itsdangerous_rs::timed::*;
use std::collections::HashMap;
use std::thread::sleep;
use std::time::Duration;

#[test]
fn test_timed_serializer_roundtrip_public() {
    let s = TimedSerializer::new("pubtimedkey");
    let mut data = HashMap::new();
    data.insert("index", 333);
    let token = s.dumps(&data);
    let (loaded, _): (HashMap<String, i32>, _) = s.loads(&token, None, false).unwrap();
    assert_eq!(loaded, data);
}

#[test]
fn test_timed_serializer_with_max_age_public() {
    let s = TimedSerializer::new("pubtimedkey");
    let mut data = HashMap::new();
    data.insert("val", 17);
    let token = s.dumps(&data);
    let (loaded, _): (HashMap<String, i32>, _) = s.loads(&token, Some(3), false).unwrap();
    assert_eq!(loaded, data);
}

#[test]
fn test_timed_serializer_bad_signature_public() {
    let s = TimedSerializer::new("pubk2");
    let result: Result<(HashMap<String, bool>, _), _> = s.loads("definitely_invalid_token", None, false);
    assert!(result.is_err());
}

#[test]
fn test_timed_signature_expired_public() {
    let s = TimedSerializer::new("expirepub");
    let mut data = HashMap::new();
    data.insert("test", true);
    let token = s.dumps(&data);
    sleep(Duration::from_millis(50));
    let result = s.loads::<HashMap<String, bool>>(&token, Some(-1), false);
    assert!(result.is_err());
}