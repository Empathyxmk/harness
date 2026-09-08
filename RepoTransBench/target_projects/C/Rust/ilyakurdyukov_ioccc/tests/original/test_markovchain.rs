#[cfg(test)]
mod tests {
    use std::fs;

    #[test]
    fn test_markovchain_input() {
        let input = "The quick brown fox jumps over the lazy dog.\n";
        assert_eq!(input, fs::read_to_string("../original/test_input.txt").unwrap());
    }

    #[test]
    fn test_markovchain_short() {
        let input = "a\n";
        assert_eq!(input, fs::read_to_string("../original/test_short.txt").unwrap());
    }

    #[test]
    fn test_markovchain_input2() {
        let input = "abcabcabc\n";
        assert_eq!(input, fs::read_to_string("../original/test_input2.txt").unwrap());
    }

    // In real tests, here you would call the Markov chain logic,
    // using `input` as input and asserting on the output.
    // But in absence of that, we at least check test setup/data.
}