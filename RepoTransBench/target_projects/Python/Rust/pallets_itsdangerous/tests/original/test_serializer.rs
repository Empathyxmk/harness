use itsdangerous_rs::serializer::*;
use std::collections::HashMap;
use tempfile::NamedTempFile;
use std::io::{Seek, SeekFrom, Write, Read};

#[test]
fn test_serializer_dumps_loads() {
    let s = Serializer::new("secret-key");
    let mut data = HashMap::new();
    data.insert("hello", "world");
    let dumped = s.dumps(&data);
    let loaded: HashMap<String, String> = s.loads(&dumped, false).unwrap();
    assert_eq!(loaded, data);
}

#[test]
fn test_serializer_loads_bad_signature() {
    let s = Serializer::new("secret-key");
    let bad_token = "bad-token";
    let res: Result<HashMap<String, String>, _> = s.loads(bad_token, false);
    assert!(res.is_err());
}

#[test]
fn test_serializer_loads_payload_variants() {
    let s = Serializer::new("secret-key");
    let mut data = HashMap::new();
    data.insert("foo", "bar");
    let dumped = s.dumps(&data);
    let loaded: HashMap<String, String> = s.loads(&dumped, false).unwrap();
    assert_eq!(loaded, data);
    let loaded_payload: HashMap<String, String> = s.loads(&dumped, true).unwrap();
    assert_eq!(loaded_payload, data);
}

#[test]
fn test_serializer_dump_and_load_to_file() {
    let s = Serializer::new("secret");
    let mut data = HashMap::new();
    data.insert("a", 1);
    data.insert("b", 2);

    let mut file = NamedTempFile::new().unwrap();
    s.dump(&data, &mut file).unwrap();
    file.seek(SeekFrom::Start(0)).unwrap(); // Rewind to start
    let loaded: HashMap<String, i32> = s.load(&mut file).unwrap();
    assert_eq!(loaded, data);
}