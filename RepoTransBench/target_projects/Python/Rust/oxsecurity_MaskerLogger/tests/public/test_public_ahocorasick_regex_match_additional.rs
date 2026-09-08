use maskerlogger::ahocorasick_regex_match::_build_ahocorasick;

#[test]
fn test_empty_trie() {
    let trie = _build_ahocorasick(vec![]);
    let matches: Vec<_> = trie.iter("this string has nothing of interest").collect();
    assert_eq!(matches, vec![]);
}

#[test]
fn test_partial_match_not_found() {
    let trie = _build_ahocorasick(vec!["dog", "cat", "mouse"]);
    let s = "The quick brown fox.";
    let found: Vec<_> = trie.iter(s).map(|(_,(_,w))| w).collect();
    assert_eq!(found, Vec::<String>::new());
}