use n0fate_chainbreaker::schema::{KeychainSchema};
#[test]
fn test_schema_get_column_names() {
    let s = KeychainSchema::default();
    let names = s.get_column_names("genp");
    assert!(!names.is_empty());
}
#[test]
fn test_schema_iter_with_disable_decode() {
    let s = KeychainSchema::default();
    let records = s.iter("genp", true);
    assert_eq!(records[0][0], 1);
}
#[test]
fn test_decode_val_bytes() {
    let s = KeychainSchema::default();
    let res = s._decode_val(Some(b"abc"));
    assert_eq!(res, Some(b"abc".to_vec()));
}
#[test]
fn test_decode_val_none() {
    let s = KeychainSchema::default();
    let res = s._decode_val(None);
    assert!(res.is_none());
}
#[test]
fn test_decode_val_str() {
    let s = KeychainSchema::default();
    let val = b"hello world";
    let r = s._decode_val(Some(val));
    assert_eq!(r, Some(val.to_vec()));
}
#[test]
fn test_repr_methods() {
    let s = KeychainSchema::default();
    let repr = format!("{:?}", s);
    assert!(repr.contains("KeychainSchema"));
}