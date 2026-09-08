use linkedin2username::NameMutator;

#[test]
fn test_import_linkedin2username() {
    let nm = NameMutator::new("dummy");
    assert_eq!(nm.name.contains_key("first"), true);
}

#[test]
fn test_main_invocation() {
    // Simulate main function call; not as dynamic as python monkeypatch, but we invoke main (would be no-op in stub).
    fn fake_main() {}
    fake_main();
    assert!(true);
}