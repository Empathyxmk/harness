// Translation of shortuuid/test_shortuuid.py

#[cfg(test)]
mod tests {
    use skorokithakis_shortuuid::*;

    #[test]
    fn test_shortuuid_instance_encode_decode() {
        let s = ShortUUID::new();
        let uuid_obj = uuid::Uuid::new_v4();
        let shortstr = s.encode(&uuid_obj);
        let decoded = s.decode(&shortstr).unwrap();
        assert_eq!(uuid_obj, decoded);
    }

    #[test]
    fn test_shortuuid_instance_alphabet() {
        let mut s = ShortUUID::new();
        let abc = "aabbcc";
        s.set_alphabet(abc);
        assert_eq!(s.get_alphabet(), abc);
        let randstr = s.random(15);
        for c in randstr.chars() {
            assert!(abc.contains(c));
        }
    }

    #[test]
    fn test_shortuuid_instance_uuid_length() {
        let s = ShortUUID::new();
        let u = s.uuid(Some(10));
        assert_eq!(u.len(), 10);
    }
}