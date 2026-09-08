use analang_como_lang_ng::io::*;

#[test]
fn test_read_line_normal() {
    set_stdin_str("hello\n");
    let line = read_line();
    assert!(line.is_some() && line.as_deref() == Some("hello"));
    clear_stdin();
}

#[test]
fn test_read_line_empty() {
    set_stdin_str("\n");
    let line = read_line();
    assert!(line.is_some() && line.as_deref() == Some(""));
    clear_stdin();
}

#[test]
fn test_read_line_eof() {
    set_stdin_none();
    let line = read_line();
    assert!(line.is_none());
    clear_stdin();
}

#[test]
fn test_read_line_error() {
    // Simulate error by setting COMO_STDIN to None
    set_stdin_none();
    let line = read_line();
    assert!(line.is_none());
    clear_stdin();
}