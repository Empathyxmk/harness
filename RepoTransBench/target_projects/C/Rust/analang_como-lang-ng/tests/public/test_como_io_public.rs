use analang_como_lang_ng::io::*;

#[test]
fn test_read_line_normal_public() {
    set_stdin_str("world\n");
    let line = read_line();
    assert!(line.is_some() && line.as_deref() == Some("world"));
    clear_stdin();
}

#[test]
fn test_read_line_all_space_public() {
    set_stdin_str("   \n");
    let line = read_line();
    assert!(line.is_some() && line.as_deref() == Some("   "));
    clear_stdin();
}

#[test]
fn test_read_line_eof_afterline_public() {
    set_stdin_str("foo\n");
    let first = read_line();
    assert!(first.is_some() && first.as_deref() == Some("foo"));
    set_stdin_none();
    let line = read_line();
    assert!(line.is_none());
    clear_stdin();
}

#[test]
fn test_read_line_error_public() {
    set_stdin_none();
    let line = read_line();
    assert!(line.is_none());
    clear_stdin();
}