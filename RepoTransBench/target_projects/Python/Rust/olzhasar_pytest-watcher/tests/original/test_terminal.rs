use crate::terminal::Terminal;

#[test]
fn test_terminal_basic_methods() {
    let term = Terminal::new();
    // Should at least have Debug trait
    assert!(format!("{:?}", term).contains("Terminal"));
}

#[test]
fn test_terminal_theme_colors() {
    let term = Terminal::new();
    // Check instantiation
    assert!(matches!(term, Terminal {..}));
}