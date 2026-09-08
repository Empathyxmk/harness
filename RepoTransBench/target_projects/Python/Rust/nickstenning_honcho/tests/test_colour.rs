use crate::colour::*;

#[test]
fn test_colours() {
    assert_eq!(RED, "31");
    assert_eq!(INTENSE_RED, "31;1");
    assert_eq!(CYAN, "36");
    assert_eq!(INTENSE_CYAN, "36;1");
}

#[test]
fn test_get_colours() {
    let names = ["cyan", "yellow", "green", "magenta", "red", "blue"];
    let mut results = vec![];
    for &name in &names {
        results.push(get_colour(name));
    }
    assert_eq!(results.len(), 6);
}