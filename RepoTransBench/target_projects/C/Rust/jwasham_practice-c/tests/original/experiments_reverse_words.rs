use jwasham_practice_c_rust::experiments::reverse_words;

#[test]
fn test_reverse_words_basic() {
    let mut s1 = String::from("My kingdom for a horse.");
    reverse_words(&mut s1);
    assert_eq!(&s1, "horse. a for kingdom My");
}

#[test]
fn test_reverse_words_empty() {
    let mut empty = String::new();
    reverse_words(&mut empty);
    assert_eq!(&empty, "");
}

#[test]
fn test_reverse_words_spaces() {
    let mut s2 = String::from(" This is  spaced ");
    reverse_words(&mut s2);
    assert_eq!(&s2, " spaced  is This ");
}

#[test]
fn test_reverse_words_failure() {
    let mut s = String::from("a");
    assert!(reverse_words(&mut s) == true);
}