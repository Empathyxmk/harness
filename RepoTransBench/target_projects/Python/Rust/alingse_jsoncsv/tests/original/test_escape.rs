use crate::utils::{encode_safe_key, decode_safe_key};

#[test]
fn test_all() {
    let path = vec!["A", "B", "..", "\\.\\ww"];
    for sep in ['A', 'B', '.', 'w'] {
        let key = encode_safe_key(&path, sep);
        let _path = decode_safe_key(&key, sep);
        assert_eq!(path, _path.iter().map(String::as_str).collect::<Vec<_>>());
    }
}

#[test]
fn test_encode() {
    let path = vec!["A", "B", "C", "www.xxx.com"];
    let sep = '.';
    let key = encode_safe_key(&path, sep);
    assert_eq!(key, "A\\.B\\.C\\.www.xxx.com");
}

#[test]
fn test_decode() {
    let key = "A\\.B\\.C\\.www.xxx.com";
    let sep = '.';
    let path = decode_safe_key(key, sep);
    assert_eq!(path[0], "A");
    assert_eq!(path[1], "B");
    assert_eq!(path[2], "C");
    assert_eq!(path[3], "www.xxx.com");
}