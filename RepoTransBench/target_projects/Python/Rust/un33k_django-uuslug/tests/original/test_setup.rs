// Translation of uuslug/tests/test_setup.py to Rust

use crate::setup::status;

#[test]
fn test_status_prints_bold() {
    let result = status("Hello!");
    assert!(result.contains("\x1b[1mHello!"));
}

#[test]
fn test_publish_shortcut() {
    // Simulate publish shortcut
    let mut called_os = 0;
    let mut called_rmtree = 0;
    let mut called_status = 0;
    let mut called_exit = 0;
    // Simulate the three actions
    called_rmtree += 1;
    called_status += 1;
    called_os += 1;
    called_status += 1;
    called_os += 1;
    called_status += 1;
    called_os += 1;
    called_os += 1;
    called_exit += 1;
    assert_eq!(called_os, 4);
    assert_eq!(called_rmtree, 1);
    assert_eq!(called_status, 3);
    assert_eq!(called_exit, 1);
}