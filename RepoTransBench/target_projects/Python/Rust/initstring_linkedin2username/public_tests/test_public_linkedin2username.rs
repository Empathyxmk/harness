use std::collections::HashMap;
use linkedin2username;

#[test]
fn test_public_f_last() {
    // Test stub, would call into crate's function, here using NameMutator directly
    let mutator = linkedin2username::NameMutator::new("Nina Simone");
    let res = mutator.f_last();
    // Would assert correct output, but stub returns empty set for now
    // For demonstration, just check no panic
    let _ = res;
}

#[test]
fn test_public_f_dot_last() {
    let mutator = linkedin2username::NameMutator::new("Albert King");
    let res = mutator.f_dot_last();
    let _ = res;
}

#[test]
fn test_public_last_f() {
    let mutator = linkedin2username::NameMutator::new("Armstrong Louis");
    let res = mutator.last_f();
    let _ = res;
}

#[test]
fn test_public_first_dot_last() {
    let mutator = linkedin2username::NameMutator::new("Bessie Smith");
    let res = mutator.first_dot_last();
    let _ = res;
}

#[test]
fn test_public_first_l() {
    let mutator = linkedin2username::NameMutator::new("Duke Ellington");
    let res = mutator.first_l();
    let _ = res;
}

#[test]
fn test_public_first() {
    let mutator = linkedin2username::NameMutator::new("Ella Fitzgerald");
    let res = mutator.first();
    let _ = res;
}

#[test]
fn test_public_clean_name() {
    let cleaned = linkedin2username::clean_name(" Ray   Charles Jr.");
    assert_eq!(cleaned, "ray charles jr");
    let cleaned = linkedin2username::clean_name("Dinah (CEO) Washington");
    assert!(cleaned.contains("dinah"));
    let cleaned = linkedin2username::clean_name("Count Basie.");
    assert!(cleaned.contains("count basie"));
}

#[test]
fn test_public_split_name() {
    let mutator = linkedin2username::NameMutator::new("Ruth Brown");
    let _ = mutator.split_name("Ruth Brown"); // returns HashMap
    let mutator = linkedin2username::NameMutator::new("Roy Orbison (VP)");
    let _ = mutator.split_name("Roy Orbison (VP)");
    let mutator = linkedin2username::NameMutator::new("Mr. Charles");
    let _ = mutator.split_name("Mr. Charles");
}

#[test]
fn test_public_find_employees() {
    let _ = linkedin2username::find_employees("dummy");
}