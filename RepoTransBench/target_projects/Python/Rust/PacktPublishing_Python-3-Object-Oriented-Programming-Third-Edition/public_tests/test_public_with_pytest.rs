#[cfg(test)]
mod tests {
    #[test]
    fn test_sum_data_public() {
        let data: Vec<i32> = (11..15).collect();
        assert_eq!(data.iter().sum::<i32>(), 50);
    }
    #[test]
    fn test_square_public() {
        let squares = vec![(2, 4), (5, 25), (10, 100)];
        for (x, expected) in squares {
            assert_eq!(x * x, expected);
        }
    }
}