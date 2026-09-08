#[cfg(test)]
mod tests {
    use std::fs;

    #[test]
    fn test_lettermixer_public_alpha() {
        let alpha_input = "hello\nworld\nabc XYZ\n";
        assert_eq!(alpha_input, fs::read_to_string("../public_tests/public_test_alpha.txt").unwrap());
    }

    #[test]
    fn test_lettermixer_public_unicode() {
        let unicode_input = "Grøvål\nßeta ÄÖÜ\nΣειρά\n";
        assert_eq!(unicode_input, fs::read_to_string("../public_tests/public_test_unicode.txt").unwrap());
    }

    #[test]
    fn test_lettermixer_public_punctuation() {
        let punc_input = "WOW! so;many:punctuation,marks?here...\n@#*&^%$!\n";
        assert_eq!(punc_input, fs::read_to_string("../public_tests/public_test_punctuation.txt").unwrap());
    }
}