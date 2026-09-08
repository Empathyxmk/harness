use itsdangerous_rs::timed::*;
use std::collections::HashMap;
use std::time::{Duration, Instant};

#[test]
fn test_timedserializer_dumps_loads() {
    let s = TimedSerializer::new("secret-key");
    let mut data = HashMap::new();
    data.insert("msg", "timed");
    let dumped = s.dumps(&data);
    let (loaded, _): (HashMap<String, String>, _) = s.loads(&dumped, None, false).unwrap();
    assert_eq!(loaded, data);
}

#[test]
fn test_timedserializer_expiry() {
    let s = TimedSerializer::new("secret-expiry");
    let mut data = HashMap::new();
    data.insert("foo", 1);
    let token = s.dumps(&data);
    let (loaded, _): (HashMap<String, i32>, _) = s.loads(&token, None, false).unwrap();
    assert_eq!(loaded, data);

    let expired = s.loads::<HashMap<String, i32>>(&token, Some(-1), false);
    assert!(expired.is_err());
}

#[test]
fn test_timedserializer_tuple_loading_options() {
    let s = TimedSerializer::new("secret-key2");
    let mut map = HashMap::new();
    map.insert("a", 2);
    let token = s.dumps(&map);
    let (result, timestamp) = s.loads::<HashMap<String, i32>>(&token, None, true).unwrap();
    assert_eq!(result, map);
    assert!(timestamp.is_some());
}

#[test]
fn test_timedserializer_bad_signature() {
    let s = TimedSerializer::new("secret");
    // Bad token
    let broken = "bad-token";
    let res = s.loads::<HashMap<String, i32>>(broken, None, false);
    assert!(res.is_err());
    // Tampered
    let mut orig_map = HashMap::new();
    orig_map.insert("foo", 42);
    let orig = s.dumps(&orig_map);
    let tampered: String = orig.chars().rev().collect();
    let res2 = s.loads::<HashMap<String, i32>>(&tampered, None, false);
    assert!(res2.is_err());
}