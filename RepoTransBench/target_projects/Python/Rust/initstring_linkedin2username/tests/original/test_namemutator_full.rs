use std::collections::{HashMap, HashSet};
use linkedin2username::NameMutator;

// Helper for test param sets - (input_name, expected_first_last map)
fn name_parametric_tests() -> Vec<(&'static str, HashMap<&'static str, &'static str>)> {
    vec![
        ("John Smith",      HashMap::from([("first", "john"),      ("second", "smith")])),
        ("Jane D'oe",       HashMap::from([("first", "jane"),      ("second", "doe")])),
        ("Dr. Ángela Gómez (MBA, PhD)", HashMap::from([("first", "angela"),   ("second", "gomez")])),
        ("Mr. François Noël", HashMap::from([("first", "francois"), ("second", "noel")])),
        ("José Niño",       HashMap::from([("first", "jose"),      ("second", "nino")])),
        ("Joe (CTO) Bloggs",HashMap::from([("first", "joe"),       ("second", "bloggs")])),
        ("Alíce O'Conñor (CISO)", HashMap::from([("first", "alice"),   ("second", "oconor")])),
        ("Mononym",         HashMap::from([("first", "mononym"),   ("second", "")])),
    ]
}

#[test]
fn test_clean_and_split_name() {
    for (input_name, expected) in name_parametric_tests() {
        let nm = NameMutator::new(input_name);
        let mut expected_map = HashMap::new();
        expected_map.insert("first".to_string(), expected["first"].to_string());
        expected_map.insert("second".to_string(), expected["second"].to_string());
        assert_eq!(nm.name, expected_map);
    }
}

// Helper for test_first parametric
fn test_first_cases() -> Vec<(&'static str, &'static str)> {
    vec![
        ("John Smith", "john"),
        (" Jane Smith ", "jane"),
        ("Dr. Ángela Gómez (MBA, PhD)", "angela"),
        ("Mononym", "mononym"),
        ("", ""),
    ]
}

#[test]
fn test_first() {
    for (input_name, expected) in test_first_cases() {
        let nm = NameMutator::new(input_name);
        assert_eq!(nm.first(), expected);
    }
}

// Helper for test_last parametric
fn test_last_cases() -> Vec<(&'static str, &'static str)> {
    vec![
        ("John Smith", "smith"),
        ("Jane D'oe", "doe"),
        ("Dr. Ángela Gómez (MBA, PhD)", "gomez"),
        ("Mr. François Noël", "noel"),
        ("José Niño", "nino"),
        ("Joe (CTO) Bloggs", "bloggs"),
        ("Alíce O'Conñor (CISO)", "oconor"),
        ("Mononym", ""),
        ("", ""),
    ]
}

#[test]
fn test_last() {
    for (input_name, expected) in test_last_cases() {
        let nm = NameMutator::new(input_name);
        assert_eq!(nm.last(), expected);
    }
}

#[test]
fn test_mutators_all_variants() {
    let nm = NameMutator::new("John O'Conner (CEO)");
    let variants: HashSet<String> = nm.mutators().into_iter().collect();
    assert!(variants.contains("johnoconner"));
    assert!(variants.contains("joconner"));
    assert!(variants.iter().any(|v| v.contains("john.o") || v.contains("johno")));
}

#[test]
fn test_name_with_empty_string() {
    let nm = NameMutator::new("");
    let mut expected = HashMap::new();
    expected.insert("first".to_string(), "".to_string());
    expected.insert("second".to_string(), "".to_string());
    assert_eq!(nm.name, expected);
    let mutators = nm.mutators();
    assert!(mutators.is_empty());
}