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
fn test_clean_and_split_name_public() {
    let samples = vec![
        ("Sam Lee", mkmap("sam", "lee", "")),
        ("Ms. Eva O'Brien", mkmap("eva", "obrien", "")),
        ("Prof. Łukasz Nowak (PhD)", mkmap("lukasz", "nowak", "")),
        ("María-José Carreño", mkmap("maria", "carreno", "")),
        ("Chris (CEO) Smithers", mkmap("chris", "smithers", "")),
    ];
    for (input, expected) in samples {
        let nm = NameMutator::new(input);
        assert_eq!(nm.name, expected);
    }
}