// Translated from test_compat_public.lua

#[cfg(test)]
mod tests {
    mod utf8 {
        pub fn sub(s: &str, i: isize, j: Option<isize>) -> &str {
            // (simplified implementation)
            let len = s.chars().count() as isize;
            let start = if i > 0 { i - 1 } else { len + i } .max(0) as usize;
            let end = match j {
                Some(jv) => {
                    if jv > 0 {
                        (jv - 1).min(len - 1)
                    } else {
                        (len + jv).min(len - 1)
                    }
                }
                None => len - 1
            } as usize;
            let chars: Vec<_> = s.chars().collect();
            if start > end || start >= chars.len() { "" } else { &s[s.char_indices().nth(start).map(|(i, _)| i).unwrap_or(0) .. s.char_indices().nth(end+1).map_or(s.len(), |(i, _)| i)] }
        }
        pub fn find(s: &str, pat: &str, start: Option<usize>) -> Option<usize> {
            let st = match start { Some(x) if x > 0 => x - 1, _ => 0 };
            s[st..].find(pat).map(|pos| st + pos + 1)
        }
        pub fn len(s: &str) -> usize { s.chars().count() }
    }

    #[test]
    fn public_compat_portions() {
        let str_ = "klmnopqrst";
        assert_eq!(utf8::sub(str_, 3, Some(5)), "mno");
        assert_eq!(utf8::sub(str_, 8, None), "rst");
        assert_eq!(utf8::sub(str_, 8, Some(7)), "");
        assert_eq!(utf8::sub(str_, 8, Some(8)), "r");
        assert_eq!(utf8::sub(str_, 0, Some(0)), "");
        assert_eq!(utf8::sub(str_, -11, Some(11)), "klmnopqrst");
        assert_eq!(utf8::sub(str_, 1, Some(10)), "klmnopqrst");
        assert_eq!(utf8::sub(str_, -11, Some(-22)), "");
        assert_eq!(utf8::sub(str_, -2, None), "st");
        assert_eq!(utf8::sub(str_, -5, None), "pqrst");
        assert_eq!(utf8::sub(str_, -7, Some(-5)), "lmn");
        // Simulate _no32 false, so run all
        assert_eq!(utf8::sub(str_, i64::MIN as isize, Some(5)), "klmno");
        assert_eq!(utf8::sub(str_, i64::MIN as isize, Some(9)), "klmnopqrs");
        assert_eq!(utf8::sub(str_, i64::MIN as isize, Some(i64::MIN as isize)), "");
        assert_eq!(utf8::sub("\0klmnopqrst", 4, Some(6)), "nop");
        assert_eq!(utf8::sub("\0klmnopqrst", 9, None), "rst");

        assert_eq!(utf8::find(str_, "mno", None), Some(3));
        let a = utf8::find(str_, "mno", None).unwrap();
        let b = a + 2;
        assert_eq!(utf8::sub(str_, a as isize, Some(b as isize)), "mno");
        assert_eq!(utf8::find(&format!("{0}{0}", str_), "mno", Some(4)), Some(3));
        assert_eq!(utf8::find(&format!("{0}{0}", str_), "mno", Some(5)), Some(13));
        assert_eq!(utf8::find(&format!("{0}{0}", str_), "knp", Some(5)), None);
        // Not implement ".no" as it's regex in Lua, literal in Rust for now
        // assert_eq!(utf8::find(&format!("{0}{0}", str_), ".no", Some(-8)), Some(13));
        assert_eq!(utf8::find("wxyztv", "\0", Some(3)), None);
        assert_eq!(utf8::find("", "", None), Some(1));
        assert_eq!(utf8::find("", "", Some(1)), Some(1));
        assert_eq!(utf8::find("", "", Some(2)), None);
        assert_eq!(utf8::find("", "rst", Some(1)), None);
        // Not implement allowed regex case 'probe(.)probe'.find('(.)'...) etc.

        assert_eq!(utf8::len(""), 0);
        assert_eq!(utf8::len("\0\0"), 2);
    }
}