use crate::runner::mountain::*;

#[test]
fn test_it_gets_test_results() {
    let mountain = Mountain::new();
    mountain.walk_the_path();
    assert!(mountain.lesson.was_learned());
}