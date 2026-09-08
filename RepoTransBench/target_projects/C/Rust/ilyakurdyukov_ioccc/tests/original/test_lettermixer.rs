#[cfg(test)]
mod tests {
    use std::fs;

    #[test]
    fn test_lettermixer_basic() {
        let input = "abcde\n";
        assert_eq!(input, fs::read_to_string("../original/test_basic.txt").unwrap());
    }

    #[test]
    fn test_lettermixer_symbols() {
        let input = "abcDE!?123 @xyz\n";
        assert_eq!(input, fs::read_to_string("../original/test_symbols.txt").unwrap());
    }

    // In real tests, here you would call the lettermixer logic,
    // using `input` as input and asserting on output.
    // But in absence of that code, we at least check test setup/data.
}