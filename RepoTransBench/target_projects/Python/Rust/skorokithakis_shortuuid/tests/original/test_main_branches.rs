// Translation of shortuuid/test_main_branches.py

#[cfg(test)]
mod tests {
    use skorokithakis_shortuuid::*;

    #[test]
    fn test_uuid_with_length() {
        let s = uuid(Some(8));
        assert_eq!(s.len(), 8);
    }

    #[test]
    fn test_uuid_without_length() {
        let s = uuid(None);
        assert!(s.len() > 0, "uuid should produce nonempty string");
    }

    #[test]
    fn test_encode_decode_roundtrip() {
        let uuid_obj = uuid::Uuid::new_v4();
        let encoded = encode(&uuid_obj);
        let decoded = decode(&encoded).unwrap();
        assert_eq!(uuid_obj, decoded);
    }

    #[test]
    fn test_decode_invalid_error() {
        let r = decode("____INVALID___");
        assert!(r.is_err());
    }
}