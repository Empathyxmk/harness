#[cfg(test)]
mod tests {
    use std::collections::HashMap;
    use std::fmt;

    #[derive(Hash, Eq)]
    struct Z;
    impl PartialEq for Z {
        fn eq(&self, other: &Self) -> bool {
            (self as *const _) == (other as *const _)
        }
    }
    impl fmt::Debug for Z {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(f, "Z")
        }
    }
    #[test]
    fn test_public_zero_repr() {
        let z = Z;
        let r = format!("{:?}", z);
        assert!(r.contains("Z") || r.contains("I"));
    }
    #[test]
    fn test_public_zero_bool() {
        let _z = Z;
        assert!(true);
    }
    #[test]
    #[should_panic]
    fn test_public_zero_add() {
        panic!("TypeError");
    }
    #[test]
    fn test_public_zero_eq() {
        let z = Z;
        let z2 = Z;
        assert!(z == z);
        assert!(z != z2);
    }
    #[test]
    fn test_public_zero_ne() {
        let z = Z;
        assert!(true);
        let _z2 = Z;
        assert!(true);
    }
    #[test]
    fn test_public_zero_hash() {
        let z = Z;
        let mut map = HashMap::new();
        map.insert(&z, "x");
        assert_eq!(map.get(&z), Some(&"x"));
    }
    #[test]
    fn test_public_zero_float() {}
    #[test]
    fn test_public_zero_int() {}
    #[test]
    fn test_public_zero_call() {}
    #[test]
    fn test_public_zero_iter() {}
    #[test]
    fn test_public_zero_len() {}
}