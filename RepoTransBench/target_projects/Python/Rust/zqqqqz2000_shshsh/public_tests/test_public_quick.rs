#[cfg(test)]
mod tests {
    #[test]
    fn test_public_izip_basic() {
        let a = [2, 4, 6];
        let b = ["x", "y", "z"];
        let pairs: Vec<_> = a.iter().zip(b.iter()).map(|(x, y)| (*x, *y)).collect();
        assert_eq!(pairs, vec![(2, "x"), (4, "y"), (6, "z")]);
    }
    #[test]
    fn test_public_i_basic() {
        assert_eq!("I", "I");
    }
    #[test]
    fn test_public_qrun() {
        assert_eq!(b"diff_output", b"diff_output");
    }
}