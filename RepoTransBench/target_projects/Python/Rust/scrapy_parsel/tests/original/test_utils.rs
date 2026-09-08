// Rust translation of tests/test_utils.py

#[cfg(test)]
mod tests {
    use super::*;
    use crate::utils::{shorten, extract_regex};

    #[test]
    fn test_shorten_cases() {
        let cases = vec![
            (-1, None), // should error
            (0, Some("".to_string())),
            (1, Some(".".to_string())),
            (2, Some("..".to_string())),
            (3, Some("...".to_string())),
            (4, Some("f...".to_string())),
            (5, Some("fo...".to_string())),
            (6, Some("foobar".to_string())),
            (7, Some("foobar".to_string())),
        ];
        for (width, expected) in cases {
            match expected {
                Some(expected_str) => assert_eq!(shorten("foobar", width).unwrap(), expected_str),
                None => assert!(shorten("foobar", width).is_err()),
            }
        }
    }

    #[test]
    fn test_extract_regex_cases() {
        let cases = vec![
            (r"(?P<month>\w+)\s*(?P<day>\d+)\s*\,?\s*(?P<year>\d+)", "October  25, 2019", true, vec!["October", "25", "2019"]),
            (r"(?P<month>\w+)\s*(?P<day>\d+)\s*\,?\s*(?P<year>\d+)", "October  25 2019", true, vec!["October", "25", "2019"]),
            (r"(?P<extract>\w+)\s*(?P<day>\d+)\s*\,?\s*(?P<year>\d+)", "October  25 2019", true, vec!["October"]),
            (r"\w+\s*\d+\s*\,?\s*\d+", "October  25 2019", true, vec!["October  25 2019"]),
            (r"^.*$", "&quot;sometext&quot; &amp; &quot;moretext&quot;", true, vec!["\"sometext\" &amp; \"moretext\""]),
            (r"^.*$", "&quot;sometext&quot; &amp; &quot;moretext&quot;", false, vec!["&quot;sometext&quot; &amp; &quot;moretext&quot;"]),
        ];
        for (regex, text, replace_entities, expected) in cases {
            let result = extract_regex(regex, text, replace_entities).unwrap();
            assert_eq!(result, expected, "regex: {}", regex);
        }
    }
}