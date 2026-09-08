use crate::terminal::Terminal;

#[test]
fn test_terminal_type_and_methods() {
    let term = Terminal::new();
    assert!(format!("{}", term).contains("pytest_watcher"));
}

#[test]
fn test_terminal_instance_not_false() {
    let term = Terminal::new();
    assert!(std::mem::size_of_val(&term) > 0);
}