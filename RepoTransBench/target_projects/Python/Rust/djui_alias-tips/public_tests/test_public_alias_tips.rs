// Rust translation of public_tests/test_public_alias_tips.py

use alias_tips::{suggest_alias, is_alias_recommended, CommandArg};

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;

    #[test]
    fn test_suggest_alias_known_variants() {
        // Should NOT match - casing or ordering or superstring
        assert_eq!(suggest_alias("List"), None); // different case
        assert_eq!(suggest_alias("Remove files"), None); // superstring
        assert_eq!(suggest_alias("directory make"), None); // reversed wording
        assert_eq!(suggest_alias("MOVE"), None); // allcaps
    }

    #[test]
    fn test_suggest_alias_none_variants() {
        assert_eq!(suggest_alias(" list "), None); // leading/trailing space
        assert_eq!(suggest_alias("copy files"), None); // superstring
        assert_eq!(suggest_alias("Make Directory"), None); // casing
        assert_eq!(suggest_alias("mv"), None); // alias itself

        assert_eq!(suggest_alias(0), None); // another type
        let dummy_map: HashMap<String,String> = HashMap::new();
        assert_eq!(suggest_alias(&dummy_map), None); // another type
    }

    #[test]
    fn test_is_alias_recommended_true_and_false() {
        assert!(is_alias_recommended("move"));
        assert!(is_alias_recommended("copy"));

        assert!(!is_alias_recommended("Move")); // casing
        assert!(!is_alias_recommended("copy file")); // superstring
        assert!(!is_alias_recommended("make  directory")); // extra space
        assert!(!is_alias_recommended("ls")); // alias itself

        let dummy_map: HashMap<String,String> = HashMap::new();
        assert!(!is_alias_recommended(&dummy_map)); // wrong type
        assert!(!is_alias_recommended(999)); // int
    }
}