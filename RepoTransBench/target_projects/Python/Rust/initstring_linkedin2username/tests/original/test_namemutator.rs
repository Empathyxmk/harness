use std::collections::HashMap;
use linkedin2username::NameMutator;

fn mkmap(first: &str, last: &str, second: &str) -> HashMap<String, String> {
    let mut h = HashMap::new();
    h.insert("first".to_string(), first.to_string());
    h.insert("last".to_string(), last.to_string());
    h.insert("second".to_string(), second.to_string());
    h
}

#[test]
fn test_clean_and_split_name() {
    let samples = vec![
        ("John Smith", mkmap("john", "smith", "")),
        ("Jane D'oe", mkmap("jane", "doe", "")),
        ("Dr. Ángela Gómez (MBA, PhD)", mkmap("angela", "gomez", "")),
        ("José Niño", mkmap("jose", "nino", "")),
        ("Joe (CTO) Bloggs", mkmap("joe", "bloggs", "")),
    ];
    for (input, expected) in samples {
        let nm = NameMutator::new(input);
        assert_eq!(nm.name, expected);
    }
}