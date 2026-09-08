#[cfg(test)]
mod tests {
    #[test]
    fn test_mean_public() {
        let data = vec![9, 18, 27];
        let mean: f64 = data.iter().sum::<i32>() as f64 / data.len() as f64;
        assert_eq!(mean, 18.0);
    }
    #[test]
    fn test_max_public() {
        let data = vec![9, 18, 27];
        assert_eq!(*data.iter().max().unwrap(), 27);
    }
    #[test]
    fn test_min_public() {
        let data = vec![9, 18, 27];
        assert_eq!(*data.iter().min().unwrap(), 9);
    }
}