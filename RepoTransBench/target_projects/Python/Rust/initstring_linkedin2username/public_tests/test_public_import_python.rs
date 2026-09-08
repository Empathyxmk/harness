#[test]
fn test_public_basic_imports() {
    // In Rust, importing a module means using the crate; confirm NameMutator struct exists
    use linkedin2username::NameMutator;
    let _ = NameMutator::new("Sam");
}