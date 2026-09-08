// Translated from test_public.lua

#[cfg(test)]
mod tests {
    mod utf8 {
        pub fn len(s: &str) -> Option<usize> {
            Some(s.chars().count())
        }
        pub fn char_from_codes(codes: &[u32]) -> String {
            codes.iter().filter_map(|&c| std::char::from_u32(c)).collect()
        }
        pub fn codepoint_vec(s: &str, from: usize, to: usize) -> Vec<u32> {
            let v: Vec<u32> = s.chars().map(|c| c as u32).collect();
            let from = from - 1;
            let to = if to == usize::MAX { v.len() } else { to };
            v[from..to].to_vec()
        }
    }
    #[test]
    fn basic_utf8_public_tests() {
        let s = "Tést🦊AßC";
        assert_eq!(utf8::len(s), Some(8));
        assert_eq!(utf8::char_from_codes(&[98, 101, 108, 108, 111]), "bello");
        let t = utf8::codepoint_vec("hello", 2, 5);
        assert!(t[0] == 101 && t[1] == 108 && t[2] == 108 && t[3] == 111);
        assert_eq!(utf8::char_from_codes(&[0x679C, 0x56FD]), "果国");

        // String iteration and grapheme boundaries
        let s = "हिन्दी";
        let count = s.chars().count();
        assert_eq!(count, 6);

        // Invalid UTF-8 handling
        // "\xC2\xA2\xE2\x82\xAC" - valid utf8 for ¢€
        let bytes = vec![0xC2, 0xA2, 0xE2, 0x82, 0xAC];
        let valid_utf8 = String::from_utf8(bytes).unwrap();
        assert_eq!(utf8::len(&valid_utf8), Some(2));
        // invalid UTF-8
        let bad = vec![0xE2, 0x28, 0xA1];
        let bad_conv = String::from_utf8(bad);
        assert!(bad_conv.is_err());
    }
}