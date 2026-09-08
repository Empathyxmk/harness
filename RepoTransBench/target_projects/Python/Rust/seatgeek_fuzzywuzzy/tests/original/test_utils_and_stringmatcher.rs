use seatgeek_fuzzywuzzy::utils;
use seatgeek_fuzzywuzzy::string_processing::StringProcessor;

#[test]
fn test_validate_string_str_and_none() {
    assert!(utils::validate_string(&"abc"));
    // Rust is statically typed so None for String is not applicable, but you can simulate with Option
    // Here we'd always get 'true' with our stub
    // To model rejection:
    //assert!(!utils::validate_string(&None)); // Not applicable directly
    assert!(!utils::validate_string(&123.to_string()));
    assert!(!utils::validate_string(&vec![].len().to_string()));
}

#[test]
fn test_make_type_consistent_str() {
    let (s1, s2) = utils::make_type_consistent("abc", "def");
    assert!(s1.is_ascii());
    assert!(s2.is_ascii());
}

#[test]
fn test_intr_behavior() {
    assert_eq!(utils::intr(3.7), 4);
    assert_eq!(utils::intr(3.3), 3);
    // Rust will NOT compile a function expecting f64 for a string, so can't test as Python
    // Use result type to simulate error
    let res = std::panic::catch_unwind(|| { utils::intr("42".parse().unwrap()); });
    assert!(res.is_err());
}

#[test]
fn test_asciidammit_ascii() {
    assert_eq!(utils::asciidammit("hello"), "hello");
}

#[test]
fn test_asciionly_basic() {
    assert_eq!(utils::asciionly("TeSt"), "TeSt");
    assert_eq!(utils::asciionly("abc✓"), "abc"); // '✓' removed
}

#[test]
fn test_full_process_options() {
    let s = " This is Ünicode!   ";
    let processed = utils::full_process(s, false);
    assert!(processed.to_lowercase().contains("ünicod"));
    let processed_ascii = utils::full_process(s, true);
    assert!(processed_ascii.to_lowercase().contains("nicode"));

    assert_eq!(utils::full_process("", true), "");
    assert_eq!(utils::full_process("   ", true), "");
}

#[test]
fn test_strip_and_case() {
    let s = "  hello\n";
    assert_eq!(StringProcessor::strip(s), s.trim());
    assert_eq!(StringProcessor::to_lower_case(s), s.to_lowercase());
    assert_eq!(StringProcessor::to_upper_case(s), s.to_uppercase());
}