// Translation of shortuuid/test_main_additional.py

#[cfg(test)]
mod tests {
    use skorokithakis_shortuuid::*;

    #[test]
    fn test_random_string_length_and_alphabet() {
        let len = 15;
        let s = random(len);
        assert_eq!(s.len(), len);
        // Should only contain characters from the alphabet
        let alphabet: Vec<char> = get_alphabet().chars().collect();
        for c in s.chars() {
            assert!(alphabet.contains(&c), "char '{}' not in alphabet", c);
        }
    }

    #[test]
    fn test_set_alphabet_and_random() {
        let abc = "abcdef";
        set_alphabet(abc);
        let s = random(10);
        for c in s.chars() {
            assert!(abc.contains(c), "Alphabet not updated (char {})", c);
        }
    }
}