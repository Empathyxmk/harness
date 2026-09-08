// Rust translation of test_alias_tips.py (original/unrestricted tests)

use alias_tips::{suggest_alias, is_alias_recommended, CommandArg};

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_suggest_alias_known() {
        assert_eq!(suggest_alias("list"), Some("ls"));
        assert_eq!(suggest_alias("remove"), Some("rm"));
        assert_eq!(suggest_alias("copy"), Some("cp"));
        assert_eq!(suggest_alias("move"), Some("mv"));
        assert_eq!(suggest_alias("make directory"), Some("mkdir"));
    }

    #[test]
    fn test_suggest_alias_none() {
        assert_eq!(suggest_alias("unknown"), None);
        assert_eq!(suggest_alias(""), None);

        // Simulate None/null - use Option::<&str>::None
        let none_arg: Option<&str> = None;
        assert_eq!(suggest_alias(none_arg), None);

        // Non-str input: integer
        assert_eq!(suggest_alias(123), None);

        // Non-str input: Vec (to mimic Python list)
        let dummy: Vec<&str> = vec!["a", "b"];
        assert_eq!(suggest_alias(dummy), None);
    }

    #[test]
    fn test_is_alias_recommended_true() {
        assert!(is_alias_recommended("list"));
        assert!(is_alias_recommended("remove"));
        assert!(is_alias_recommended("copy"));
        assert!(is_alias_recommended("move"));
        assert!(is_alias_recommended("make directory"));
    }

    #[test]
    fn test_is_alias_recommended_false() {
        assert!(!is_alias_recommended("something else"));
        assert!(!is_alias_recommended(""));

        let none_arg: Option<&str> = None;
        assert!(!is_alias_recommended(none_arg));

        assert!(!is_alias_recommended(123));

        let dummy: Vec<&str> = vec![];
        assert!(!is_alias_recommended(dummy));
    }
}