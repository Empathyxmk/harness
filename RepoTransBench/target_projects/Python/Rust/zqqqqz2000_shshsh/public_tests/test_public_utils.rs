#[cfg(test)]
mod tests {
    #[test]
    fn test_public_is_list_tuple_str() {
        let v = vec![1,2,3];
        assert!(v.len() == 3);
        let t = (4,5,6);
        assert_eq!(t.0, 4);
        assert!("public_test".is_ascii());
    }
    #[test]
    fn test_public_flatten() {
        fn flatten(nested: &[&[i32]]) -> Vec<i32> {
            nested.iter().flat_map(|arr| arr.iter().copied()).collect()
        }
        let l = [&[1][..], &[2, 3, 4][..], &[5][..]];
        let flat = flatten(&l);
        assert_eq!(flat, vec![1,2,3,4,5]);
    }
    #[test]
    fn test_public_range_list() {
        let r: Vec<_> = (0..7).collect();
        assert_eq!(r, vec![0,1,2,3,4,5,6]);
    }
    #[test]
    fn test_public_patch_object() {
        struct Dummy { x: i32 }
        let mut d = Dummy { x: 0 };
        d.x = 100;
        assert_eq!(d.x, 100);
    }
}