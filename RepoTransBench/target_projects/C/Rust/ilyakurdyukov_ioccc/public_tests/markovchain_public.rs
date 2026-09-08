#[cfg(test)]
mod tests {
    use std::fs;

    #[test]
    fn test_markovchain_public_input_a() {
        let input = "the quick brown fox jumps over the lazy dog\nabcdefg hijklmnop qrstuv wxyz\n";
        assert_eq!(input, fs::read_to_string("../public_tests/public_test_input_A.txt").unwrap());
    }

    #[test]
    fn test_markovchain_public_input_b() {
        let input = "one two two three three three four four four four\n";
        assert_eq!(input, fs::read_to_string("../public_tests/public_test_input_B.txt").unwrap());
    }
}