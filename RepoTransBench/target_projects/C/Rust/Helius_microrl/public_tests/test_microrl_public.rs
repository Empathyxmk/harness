use microrl::*;
use std::sync::Mutex;
use std::cell::RefCell;

// Global variables for tracking callback execution
thread_local! {
    static EXECUTED_ARGC: RefCell<usize> = RefCell::new(0);
    static EXECUTED_ARGV: RefCell<Option<Vec<String>>> = RefCell::new(None);
}

// Dummy callbacks for microrl
fn test_execute_callback(argc: usize, argv: &[&str]) -> usize {
    EXECUTED_ARGC.with(|counter| {
        *counter.borrow_mut() = argc;
    });
    
    EXECUTED_ARGV.with(|args| {
        let mut vec = Vec::new();
        for arg in argv {
            vec.push(arg.to_string());
        }
        *args.borrow_mut() = Some(vec);
    });
    
    return argc;
}

fn test_print_callback(_str: &str) {
    // Do nothing
}

fn test_sigint_callback() {
    // Do nothing
}

#[test]
fn test_microrl_init_invocation() {
    let mut rl = MicroRL::new();
    microrl_init(&mut rl, test_print_callback);

    assert_eq!(rl.print as usize, test_print_callback as usize);
}

#[test]
fn test_microrl_set_execute() {
    let mut rl = MicroRL::new();
    microrl_init(&mut rl, test_print_callback); // uses test_print_callback
    microrl_set_execute_callback(&mut rl, test_execute_callback);

    assert_eq!(rl.execute.unwrap() as usize, test_execute_callback as usize);
}

#[test]
fn test_microrl_set_sigint() {
    let mut rl = MicroRL::new();
    microrl_init(&mut rl, test_print_callback);
    microrl_set_sigint_callback(&mut rl, test_sigint_callback);

    assert_eq!(rl.sigint.unwrap() as usize, test_sigint_callback as usize);
}

#[test]
fn test_microrl_execute_callback_invocation() {
    let mut rl = MicroRL::new();
    microrl_init(&mut rl, test_print_callback);
    microrl_set_execute_callback(&mut rl, test_execute_callback);

    EXECUTED_ARGC.with(|counter| {
        *counter.borrow_mut() = 0;
    });
    
    EXECUTED_ARGV.with(|args| {
        *args.borrow_mut() = None;
    });
    
    // Use different test data: "delta" and "echo"
    let cmd = ["delta", "echo"];
    rl.execute.unwrap()(2, &cmd);

    EXECUTED_ARGC.with(|counter| {
        assert_eq!(*counter.borrow(), 2);
    });
    
    EXECUTED_ARGV.with(|args| {
        let saved_args = args.borrow();
        assert!(saved_args.is_some());
        let argv = saved_args.as_ref().unwrap();
        assert_eq!(argv[0], "delta");
        assert_eq!(argv[1], "echo");
    });
}

// Test a boundary case: zero-argument invocation
#[test]
fn test_microrl_execute_callback_zero_args() {
    let mut rl = MicroRL::new();
    microrl_init(&mut rl, test_print_callback);
    microrl_set_execute_callback(&mut rl, test_execute_callback);

    EXECUTED_ARGC.with(|counter| {
        *counter.borrow_mut() = usize::MAX; // -1 equivalent
    });
    
    EXECUTED_ARGV.with(|args| {
        *args.borrow_mut() = None;
    });

    // Use empty argument vector
    let cmd: [&str; 0] = [];
    rl.execute.unwrap()(0, &cmd);

    EXECUTED_ARGC.with(|counter| {
        assert_eq!(*counter.borrow(), 0);
    });
    
    EXECUTED_ARGV.with(|args| {
        let saved_args = args.borrow();
        assert!(saved_args.is_some());
        let argv = saved_args.as_ref().unwrap();
        assert_eq!(argv.len(), 0);
    });
}