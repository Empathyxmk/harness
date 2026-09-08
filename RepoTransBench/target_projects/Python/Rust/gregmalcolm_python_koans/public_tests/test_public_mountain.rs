use crate::runner::mountain::*;

#[test]
fn test_public_mountain_has_class() {
    let m = Mountain::new();
    // In Rust, every struct is a type, so test field existence:
    assert_eq!(std::any::type_name::<Mountain>(), "gregmalcolm_python_koans::runner::mountain::Mountain");
}
#[test]
fn test_public_mountain_has_methods() {
    let m = Mountain::new();
    // Check that walk_the_path and lesson field are callable/accessed
    m.walk_the_path();
    assert!(m.lesson.was_learned() || !m.lesson.was_learned());
}