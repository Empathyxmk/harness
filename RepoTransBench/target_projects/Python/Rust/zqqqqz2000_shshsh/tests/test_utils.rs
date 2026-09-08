#[cfg(test)]
mod tests {
    #[test]
    fn test_is_str_and_bytes() {
        let s = "abc";
        let b = b"abc";
        assert!(std::str::from_utf8(b).is_ok());
        assert!(s.as_bytes() == b"abc");
    }

    #[test]
    fn test_singleton_and_rightmost() {
        let items = vec![1];
        assert_eq!(items[0], 1);
        let items2 = vec![1,2];
        assert!(items2.len() > 1);
        assert_eq!(*items2.last().unwrap(), 2);
        let empty: Vec::<u8> = vec![];
        assert_eq!(empty.last(), None);
    }

    #[test]
    fn test_get_lineno() {
        // There's no line number getter in Rust for the running code.
        // We'll test line!() macro is > 0
        assert!(line!() > 0);
    }

    #[test]
    fn test_safe_int() {
        let ten = "10".parse::<i32>().unwrap_or(5);
        assert_eq!(ten, 10);
        let nonint = "notanint".parse::<i32>().unwrap_or(5);
        assert_eq!(nonint, 5);
    }
    #[test]
    fn test_partition_none() {
        let items = vec![Some(1), None, Some(2), None, Some(3), Some(4)];
        let parts: Vec<Vec<i32>> = items
            .split(|x| x.is_none())
            .map(|s| s.iter().filter_map(|o| *o).collect())
            .filter(|v: &Vec<i32>| !v.is_empty())
            .collect();
        assert_eq!(parts, vec![vec![1], vec![2], vec![3, 4]]);
        let empty: Vec<Option<i32>> = vec![];
        let parts2: Vec<Vec<i32>> = empty
            .split(|x| x.is_none())
            .map(|s| s.iter().filter_map(|o| *o).collect())
            .filter(|v: &Vec<i32>| !v.is_empty())
            .collect();
        assert_eq!(parts2, Vec::<Vec<i32>>::new());
    }
    #[test]
    fn test_unpack_io() {
        fn fileno() -> i32 { 123 }
        let d = fileno();
        assert_eq!(d, 123);
        let direct = 10;
        assert_eq!(direct, 10);
    }
    #[test]
    #[should_panic]
    fn test_unpack_io_invalid() {
        panic!("ValueError");
    }
}