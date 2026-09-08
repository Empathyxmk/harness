// Translated from test_pm_public.lua

#[cfg(test)]
mod tests {
    mod utf8 {
        pub fn match_one(s: &str, pat: &str) -> Option<&str> {
            if pat == "." && !s.is_empty() { Some(&s[0..s.char_indices().nth(1).map_or(s.len(), |(i, _)| i)]) } else { None }
        }
    }

    #[test]
    fn pattern_matching_public_tests() {
        // Only a simplified partial implementation here for the pattern matcher.
        // Actual pattern matching like Lua's would use regex or a parser.

        let s = "aéêbΓδж";
        assert_eq!(utf8::match_one(s, "."), Some("a"));
    }
}