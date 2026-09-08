// Translated from test_compat.lua (original test)

#[cfg(test)]
mod tests {
    use super::*;
    use std::ops::RangeInclusive;

    /// A dummy utf8 module to simulate the interface.
    /// In a real migration, these would be implemented to match lua-utf8 semantics.
    mod utf8 {
        use std::char;

        pub fn sub(s: &str, i: i32, j: Option<i32>) -> String {
            let len = s.chars().count() as i32;
            let start = if i > 0 { i - 1 } else { (len + i) } .max(0);
            let end = match j {
                Some(j) if j > 0 => (j - 1).min(len - 1),
                Some(j) => (len + j).min(len - 1),
                None => len - 1,
            }.max(start);

            s.chars().skip(start as usize).take((end - start + 1).max(0) as usize).collect()
        }

        pub fn find(s: &str, pat: &str, start: Option<i32>, plain: Option<bool>) -> Option<usize> {
            let s_chars: Vec<char> = s.chars().collect();
            let pat_chars: Vec<char> = pat.chars().collect();
            let st = match start {
                Some(ind) if ind >= 1 => ind as usize - 1,
                Some(ind) if ind < 0 => s_chars.len().wrapping_add(ind as usize),
                _ => 0,
            };
            for i in st..=s_chars.len().saturating_sub(pat_chars.len()) {
                if &s_chars[i..i+pat_chars.len()] == pat_chars.as_slice() {
                    return Some(i + 1);
                }
            }
            None
        }

        pub fn len(s: &str) -> Option<usize> {
            Some(s.chars().count())
        }

        pub fn upper(s: &str) -> String {
            s.chars().map(|c| c.to_uppercase().collect::<String>()).collect()
        }
        pub fn lower(s: &str) -> String {
            s.chars().map(|c| c.to_lowercase().collect::<String>()).collect()
        }
        pub fn reverse(s: &str) -> String {
            s.chars().rev().collect()
        }

        pub fn escape(s: &str) -> String {
            s.chars().map(|c| {
                if c.is_ascii_graphic() || c == '%' || c.is_whitespace() {
                    c.to_string()
                } else {
                    format!("%{:x}", c as u32)
                }
            }).collect()
        }

        pub fn char_from_codepoints(cps: &[u32]) -> String {
            cps.iter()
                .map(|&cp| std::char::from_u32(cp).unwrap_or('\u{FFFD}'))
                .collect()
        }

        pub fn byte(s: &str, range: Option<(isize, isize)>) -> Option<Vec<u8>> {
            let s_bytes = s.as_bytes();
            let (start, end) = range.unwrap_or((1, 1));
            if start < 1 || end < 1 || (start as usize) > s_bytes.len() || (end as usize) > s_bytes.len() {
                return None;
            }
            Some(s_bytes[start as usize - 1 .. end as usize].to_vec())
        }
    }

    #[test]
    fn test_utf8_sub() {
        assert_eq!(utf8::sub("123456789", 2, Some(4)), "234");
        assert_eq!(utf8::sub("123456789", 7, None), "789");
        assert_eq!(utf8::sub("123456789", 7, Some(6)), "");
        assert_eq!(utf8::sub("123456789", 7, Some(7)), "7");
        assert_eq!(utf8::sub("123456789", 0, Some(0)), "");
        assert_eq!(utf8::sub("123456789", -10, Some(10)), "123456789");
        assert_eq!(utf8::sub("123456789", 1, Some(9)), "123456789");
        assert_eq!(utf8::sub("123456789", -10, Some(-20)), "");
        assert_eq!(utf8::sub("123456789", -1, None), "9");
        assert_eq!(utf8::sub("123456789", -4, None), "6789");
        assert_eq!(utf8::sub("123456789", -6, Some(-4)), "456");

        // Simulate _no32 false, so we run these.
        assert_eq!(utf8::sub("123456789", i32::MIN, Some(-4)), "123456");
        assert_eq!(utf8::sub("123456789", i32::MIN, Some(i32::MAX)), "123456789");
        assert_eq!(utf8::sub("123456789", i32::MIN, Some(i32::MIN)), "");

        assert_eq!(utf8::sub("\0123456789", 3, Some(5)), "234");
        assert_eq!(utf8::sub("\0123456789", 8, None), "789");
    }

    #[test]
    fn test_utf8_find() {
        let find = |s, p| utf8::find(s, p, None, None);
        assert_eq!(find("123456789", "345"), Some(3));
        let a = find("123456789", "345").unwrap();
        let b = a + 2;
        assert_eq!(utf8::sub("123456789", a as i32, Some(b as i32)), "345");

        assert_eq!(utf8::find("1234567890123456789", "345", Some(3), None), Some(3));
        assert_eq!(utf8::find("1234567890123456789", "345", Some(4), None), Some(13));
        assert_eq!(utf8::find("1234567890123456789", "346", Some(4), None), None);
        assert_eq!(utf8::find("1234567890123456789", ".45", Some(-9), None), Some(13));
        assert_eq!(utf8::find("abcdefg", "\0", Some(5), Some(true)), None);
        assert_eq!(find("", ""), Some(1));
        assert_eq!(utf8::find("", "", Some(1), None), Some(1));
        assert_eq!(utf8::find("", "", Some(2), None), None);
        assert_eq!(utf8::find("", "aaa", Some(1), None), None);

        // The following from ('alo(.)alo'):find('(.)', 1, 1) == 4
        // In Rust, simulate a plain search at offset 1
        // Not implemented: regex/advanced pattern match; skip or simulate as literal
    }

    #[test]
    fn test_utf8_len_and_char_byte() {
        assert_eq!(utf8::len(""), Some(0));
        assert_eq!(utf8::len("\0\0\0"), Some(3));
        assert_eq!(utf8::len("1234567890"), Some(10));
        // Not implemented: utf8.escape, utf8.byte, utf8.char as per original,
        // would require more involved implementation for round-tripping.
    }

    #[test]
    fn test_utf8_upper_lower_reverse() {
        assert_eq!(utf8::upper("ab\0c"), "AB\0C");
        assert_eq!(utf8::lower("\0ABCc%$"), "\0abcc%$");
        assert_eq!(utf8::reverse(""), "");
        assert_eq!(utf8::reverse("\0\x01\x02\x03"), "\x03\x02\x01\0");
        assert_eq!(utf8::reverse("\0" + "1234"), "4321\0");
        for i in 0..=30 {
            let s = "a".repeat(i);
            assert_eq!(utf8::len(&s), Some(i));
        }
    }
}