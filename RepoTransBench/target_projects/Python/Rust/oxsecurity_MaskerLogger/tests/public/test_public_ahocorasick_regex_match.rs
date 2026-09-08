use maskerlogger::ahocorasick_regex_match::{_build_ahocorasick, load_regexes_from_config};

#[test]
fn test_build_trie_and_match() {
    let keys = vec!["bear", "wolf", "lion"];
    let trie = _build_ahocorasick(keys.clone());
    let s = "the wolf and lion bear witness";
    let mut found = vec![];
    for (_, (_, word)) in trie.iter(&s) {
        found.push(word);
    }
    let mut expected = vec!["wolf".to_string(), "lion".to_string(), "bear".to_string()];
    found.sort();
    expected.sort();
    assert_eq!(found, expected);
}

#[test]
fn test_build_regex_from_config() {
    let result = load_regexes_from_config();
    assert!(result.is_empty() == false);
}