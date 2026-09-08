#[cfg(test)]
mod tests {
    #[test]
    fn test_mean_new_data() {
        let data = vec![10, 20, 30, 40];
        let mean: f64 = data.iter().sum::<i32>() as f64 / data.len() as f64;
        assert_eq!(mean, 25.0);
    }

    #[test]
    fn test_len_is_len() {
        let data = vec![11, 15, 21];
        assert_eq!(data.len(), 3);
    }

    #[test]
    fn test_sum_public() {
        let data = vec![4, 5, 7];
        assert_eq!(data.iter().sum::<i32>(), 16);
    }
}