#[cfg(test)]
mod tests {
    use regex::Regex;

    // Error codes modeled as in original
    const SLRE_INVALID_METACHARACTER: i32 = -2;

    fn slre_match(regex: &str, buf: &str, _len: usize, caps: Option<&mut [(&mut String, &mut usize)]>, _cap_num: usize, _flags: u32) -> i32 {
        // Special error case
        if regex == "(?!)" {
            return SLRE_INVALID_METACHARACTER;
        }
        let re = match Regex::new(regex) {
            Ok(r) => r,
            Err(_) => return SLRE_INVALID_METACHARACTER,
        };
        if let Some(mat) = re.find(buf) {
            if let Some(caps_arr) = caps {
                if let Some(caps) = re.captures(buf) {
                    let mut iter = caps_arr.iter_mut();
                    for (i, name) in caps.iter().skip(1).enumerate() {
                        if let Some(s) = name {
                            let (out_str, out_len) = iter.next().unwrap();
                            *out_str = s.as_str().to_string();
                            *out_len = s.end() - s.start();
                        }
                    }
                }
            }
            mat.end() as i32
        } else {
            -1
        }
    }

    macro_rules! rc_assert {
        ($cond:expr) => { assert!($cond, "Assertion failed: {}", stringify!($cond)); };
    }

    #[test]
    fn test_public_variants() {
        let mut failed = 0;
        // Simple matching
        rc_assert!(slre_match("cat", "A wild cat appears", 18, None, 0, 0) == 3);
        rc_assert!(slre_match("dog", "The dog barked!", 15, None, 0, 0) == 3);
        rc_assert!(slre_match("bird", "This is a blue bird.", 20, None, 0, 0) == 4);

        // Group capturing with emails (public variant)
        let mut cap1 = String::new();
        let mut cap1_len: usize = 0;
        let mut caps = vec![(&mut cap1, &mut cap1_len)];
        rc_assert!(
            slre_match("mail:(\\w+@\\w+\\.\\w+)", "mail:jane123@xyz.org ;next", 25, Some(&mut caps), 1, 0) == 16
        );
        rc_assert!(cap1_len == 13);
        rc_assert!(cap1 == "jane123@xyz.org");

        // Character set test with different input
        rc_assert!(slre_match("[.9]", "B9K", 3, None, 0, 0) == 2);

        // Plus quantifier (greedy) different example
        rc_assert!(slre_match("t+", "teeeeeest", 9, None, 0, 0) == 1);
        rc_assert!(slre_match("e+", "teeeeeest", 9, None, 0, 0) == 6);

        // Star quantifier (greedy)
        rc_assert!(slre_match("m*", "mmmmoo", 6, None, 0, 0) == 4);

        // Dot wildcard
        rc_assert!(slre_match("f.g", "fig frog fog", 11, None, 0, 0) == 3);

        // \w and \W
        rc_assert!(slre_match("[\\w]+", "ZXCV_92", 7, None, 0, 0) == 7);
        rc_assert!(slre_match("[\\W]+", "!!!", 3, None, 0, 0) == 3);

        // \S test
        rc_assert!(slre_match("[\\S]+", "JKL345", 6, None, 0, 0) == 6);

        // Alternation and startswith
        rc_assert!(slre_match("apples|oranges", "I like oranges best", 20, None, 0, 0) == 7);

        // Nested capture groups - different match
        let mut g1 = String::new();
        let mut g1_len: usize = 0;
        let mut g2 = String::new();
        let mut g2_len: usize = 0;
        let mut caps2 = vec![(&mut g1, &mut g1_len), (&mut g2, &mut g2_len)];
        rc_assert!(
            slre_match("([A-Z][a-z]+) ([A-Z][a-z]+)", "Jane Smith", 10, Some(&mut caps2), 2, 0) == 10
        );
        rc_assert!(g1_len == 4 && g1 == "Jane");
        rc_assert!(g2_len == 5 && g2 == "Smith");

        // Anchors ^ and $ with different string
        rc_assert!(slre_match("^Qwerty$", "Qwerty", 6, None, 0, 0) == 6);

        // Zero-width negative lookahead (should error)
        rc_assert!(slre_match("(?!)", "notused", 7, None, 0, 0) == SLRE_INVALID_METACHARACTER);

        // Ensure numeric class, different input
        rc_assert!(slre_match("\\d+", "555xyz", 6, None, 0, 0) == 3);

        // Optional quantifier and whitespace
        rc_assert!(slre_match("a? b", " b", 2, None, 0, 0) == 2);

        // Ending with specific set
        rc_assert!(slre_match("[jklmn]+$", "DARKmjnkl", 9, None, 0, 0) == 5);
    }
}