use linkedin2username::NameMutator;

#[test]
fn test_public_import_linkedin2username() {
    let nm = NameMutator::new("Lena Horne");
    assert!(nm.name.contains_key("first"));
}

#[test]
fn test_public_main_invocation() {
    // In Rust, we simply check we can run main and it doesn't panic
    super::super::main();
}