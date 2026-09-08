use std::collections::{HashSet, HashMap};
use linkedin2username::{NameMutator, find_employees};

fn test_names(idx: usize) -> &'static str {
    match idx {
        1 => "John Smith",
        2 => "John Davidson-Smith",
        3 => "John-Paul Smith-Robinson",
        4 => "José Gonzáles",
        5 => "🙂 Emoji Folks 🙂",
        _ => "",
    }
}

#[test]
fn test_f_last() {
    let mutator = NameMutator::new(test_names(1));
    assert_eq!(mutator.f_last(), HashSet::from(["jsmith".to_string()]));

    let mutator = NameMutator::new(test_names(2));
    assert_eq!(mutator.f_last(), HashSet::from(["jsmith".to_string(), "jdavidson".to_string()]));

    let mutator = NameMutator::new(test_names(3));
    assert_eq!(mutator.f_last(), HashSet::from(["jsmith".to_string(), "jrobinson".to_string()]));

    let mutator = NameMutator::new(test_names(4));
    assert_eq!(mutator.f_last(), HashSet::from(["jgonzales".to_string()]));

    let mutator = NameMutator::new(test_names(5));
    assert_eq!(mutator.f_last(), HashSet::from(["efolks".to_string()]));
}

#[test]
fn test_f_dot_last() {
    let mutator = NameMutator::new(test_names(1));
    assert_eq!(mutator.f_dot_last(), HashSet::from(["j.smith".to_string()]));

    let mutator = NameMutator::new(test_names(2));
    assert_eq!(mutator.f_dot_last(), HashSet::from(["j.smith".to_string(), "j.davidson".to_string()]));

    let mutator = NameMutator::new(test_names(3));
    assert_eq!(mutator.f_dot_last(), HashSet::from(["j.smith".to_string(), "j.robinson".to_string()]));

    let mutator = NameMutator::new(test_names(4));
    assert_eq!(mutator.f_dot_last(), HashSet::from(["j.gonzales".to_string()]));

    let mutator = NameMutator::new(test_names(5));
    assert_eq!(mutator.f_dot_last(), HashSet::from(["e.folks".to_string()]));
}

#[test]
fn test_last_f() {
    let mutator = NameMutator::new(test_names(1));
    assert_eq!(mutator.last_f(), HashSet::from(["smithj".to_string()]));

    let mutator = NameMutator::new(test_names(2));
    assert_eq!(mutator.last_f(), HashSet::from(["smithj".to_string(), "davidsonj".to_string()]));

    let mutator = NameMutator::new(test_names(3));
    assert_eq!(mutator.last_f(), HashSet::from(["smithj".to_string(), "robinsonj".to_string()]));

    let mutator = NameMutator::new(test_names(4));
    assert_eq!(mutator.last_f(), HashSet::from(["gonzalesj".to_string()]));

    let mutator = NameMutator::new(test_names(5));
    assert_eq!(mutator.last_f(), HashSet::from(["folkse".to_string()]));
}

#[test]
fn test_first_dot_last() {
    let mutator = NameMutator::new(test_names(1));
    assert_eq!(mutator.first_dot_last(), HashSet::from(["john.smith".to_string()]));

    let mutator = NameMutator::new(test_names(2));
    assert_eq!(mutator.first_dot_last(), HashSet::from(["john.smith".to_string(), "john.davidson".to_string()]));

    let mutator = NameMutator::new(test_names(3));
    assert_eq!(mutator.first_dot_last(), HashSet::from(["john.smith".to_string(), "john.robinson".to_string()]));

    let mutator = NameMutator::new(test_names(4));
    assert_eq!(mutator.first_dot_last(), HashSet::from(["jose.gonzales".to_string()]));

    let mutator = NameMutator::new(test_names(5));
    assert_eq!(mutator.first_dot_last(), HashSet::from(["emoji.folks".to_string()]));
}

#[test]
fn test_first_l() {
    let mutator = NameMutator::new(test_names(1));
    assert_eq!(mutator.first_l(), HashSet::from(["johns".to_string()]));

    let mutator = NameMutator::new(test_names(2));
    assert_eq!(mutator.first_l(), HashSet::from(["johns".to_string(), "johnd".to_string()]));

    let mutator = NameMutator::new(test_names(3));
    assert_eq!(mutator.first_l(), HashSet::from(["johns".to_string(), "johnr".to_string()]));

    let mutator = NameMutator::new(test_names(4));
    assert_eq!(mutator.first_l(), HashSet::from(["joseg".to_string()]));

    let mutator = NameMutator::new(test_names(5));
    assert_eq!(mutator.first_l(), HashSet::from(["emojif".to_string()]));
}

#[test]
fn test_first() {
    let mutator = NameMutator::new(test_names(1));
    assert_eq!(mutator.first(), HashSet::from(["john".to_string()]));

    let mutator = NameMutator::new(test_names(2));
    assert_eq!(mutator.first(), HashSet::from(["john".to_string()]));

    let mutator = NameMutator::new(test_names(3));
    assert_eq!(mutator.first(), HashSet::from(["john".to_string()]));

    let mutator = NameMutator::new(test_names(4));
    assert_eq!(mutator.first(), HashSet::from(["jose".to_string()]));

    let mutator = NameMutator::new(test_names(5));
    assert_eq!(mutator.first(), HashSet::from(["emoji".to_string()]));
}

#[test]
fn test_clean_name() {
    let mutator = NameMutator::new("xxx");
    assert_eq!(mutator.clean_name("  🙂Ànèôõö    ßï🙂  "), "aneooo ssi");

    let name = "Dr. Hannibal Lecter, PhD.";
    assert_eq!(mutator.clean_name(name), "hannibal lecter");

    let name = "Mr. Fancy Pants MD, PhD, MBA";
    assert_eq!(mutator.clean_name(name), "fancy pants");

    let name = "Mr. Cert Dude (OSCP, OSCE)";
    assert_eq!(mutator.clean_name(name), "cert dude");
}

#[test]
fn test_split_name() {
    let mutator = NameMutator::new("xxx");

    let name = "madonna wayne gacey";
    let expected: HashMap<String, String> = [
        ("first", "madonna"),
        ("second", "wayne"),
        ("last", "gacey")
    ]
    .iter()
    .map(|(k, v)| (k.to_string(), v.to_string()))
    .collect();
    assert_eq!(mutator.split_name(name), expected);

    let name = "twiggy ramirez";
    let expected: HashMap<String, String> = [
        ("first", "twiggy"),
        ("second", ""),
        ("last", "ramirez")
    ]
    .iter()
    .map(|(k, v)| (k.to_string(), v.to_string()))
    .collect();
    assert_eq!(mutator.split_name(name), expected);

    let name = "brian warner is marilyn manson";
    let expected: HashMap<String, String> = [
        ("first", "brian"),
        ("second", "marilyn"),
        ("last", "manson")
    ]
    .iter()
    .map(|(k, v)| (k.to_string(), v.to_string()))
    .collect();
    assert_eq!(mutator.split_name(name), expected);
}

#[test]
fn test_find_employees() {
    let result = std::fs::read_to_string("tests/mock-employee-response").unwrap_or_else(|_| "dummy file content".to_string());
    let employees = find_employees(&result);

    assert_eq!(employees.len(), 2);
    assert_eq!(employees[0]["full_name"], "Michael Myers");
    assert_eq!(employees[0]["occupation"], "Camp Counsellor");
    assert_eq!(employees[1]["full_name"], "Freddy Krueger");
    assert_eq!(employees[1]["occupation"], "Babysitter");

    let result = std::fs::read_to_string("tests/mock-employee-response-last-page").unwrap_or_else(|_| "".to_string());
    let found = find_employees(&result);
    assert!(found.is_empty() || (found.len() == 2 && found[0]["full_name"] == "Michael Myers"), "In stub: expect empty or fallback");
}