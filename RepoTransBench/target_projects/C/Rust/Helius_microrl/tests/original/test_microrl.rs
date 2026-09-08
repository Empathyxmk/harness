use microrl::*;
use std::sync::Mutex;
use std::cell::RefCell;

// Static buffer for the print callback
thread_local! {
    static PRINT_BUFFER: RefCell<String> = RefCell::new(String::new());
}

// Test print callback
fn test_print(s: &str) {
    PRINT_BUFFER.with(|buffer| {
        *buffer.borrow_mut() = s.to_string();
    });
}

// Helper to get print buffer contents
fn get_print_buffer() -> String {
    PRINT_BUFFER.with(|buffer| {
        buffer.borrow().clone()
    })
}

// Tests
#[test]
fn test_init_default() {
    let mut rl = MicroRL::new();
    microrl_init(&mut rl, test_print);
    
    assert_eq!(rl.print as usize, test_print as usize);
    assert_eq!(rl.prompt_str, ">");
    assert_eq!(rl.cmdlen, 0);
}

#[test]
fn test_set_echo() {
    microrl_set_echo(false);
    microrl_set_echo(true);
    // No return, just exercise both branches
}

#[test]
fn test_insert_char_alnum() {
    let mut rl = MicroRL::new();
    microrl_init(&mut rl, test_print);
    
    // Clear the struct
    rl = MicroRL::new();
    rl.print = test_print;
    rl.cmdlen = 0;
    
    microrl_insert_char(&mut rl, 'X');
    assert_eq!(rl.cmdline[0], 'X');
    assert_eq!(rl.cmdlen, 1);
    assert_eq!(get_print_buffer(), "X");
}

#[test]
fn test_insert_char_overflow_and_ctrlc() {
    let mut rl = MicroRL::new();
    microrl_init(&mut rl, test_print);
    
    rl.print = test_print;
    rl.cmdlen = _COMMAND_LINE_LEN - 1;
    
    // Should not add
    microrl_insert_char(&mut rl, 'Z');
    assert_eq!(rl.cmdline[rl.cmdlen], '\0');
    
    // Insert control char
    microrl_insert_char(&mut rl, KEY_ETX);
    assert_eq!(get_print_buffer(), "^C\n");
}

#[test]
fn test_split_basic() {
    let buf = "cmd one two";
    let args = microrl_split(buf, ' ');
    
    assert_eq!(args.len(), 3);
    assert_eq!(args[0], "cmd");
    assert_eq!(args[1], "one");
    assert_eq!(args[2], "two");
}

#[test]
fn test_split_edge() {
    let buf = "  a  b ";
    let args = microrl_split(buf, ' ');
    
    assert_eq!(args.len(), 2);
    assert_eq!(args[0], "a");
    assert_eq!(args[1], "b");

    let empty = "";
    let args = microrl_split(empty, ' ');
    assert_eq!(args.len(), 0);

    let space = "      ";
    let args = microrl_split(space, ' ');
    assert_eq!(args.len(), 0);

    let nospace = "token";
    let args = microrl_split(nospace, ',');
    assert_eq!(args.len(), 1);
    assert_eq!(args[0], "token");
}

#[test]
fn test_set_execute_and_complete() {
    let mut rl = MicroRL::new();
    microrl_init(&mut rl, test_print);
    
    fn dummy_execute(_argc: usize, _argv: &[&str]) -> usize { _argc }
    fn dummy_complete(_argc: usize, _argv: &[&str]) -> Option<Vec<String>> { None }
    
    microrl_set_execute_callback(&mut rl, dummy_execute);
    microrl_set_complete_callback(&mut rl, dummy_complete);
    
    assert_eq!(rl.execute.unwrap() as usize, dummy_execute as usize);
    assert_eq!(rl.get_completion.unwrap() as usize, dummy_complete as usize);
}