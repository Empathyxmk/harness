use pypa_sampleproject::appinit;
use std::cell::RefCell;

thread_local! {
    static LAST_PRINT: RefCell<Option<String>> = RefCell::new(None);
}

fn with_intercepted_print<F: FnOnce()>(f: F) -> Option<String> {
    use std::io::{self, Write};
    use std::sync::Mutex;
    use std::fmt::Arguments;

    static PRINT_MUTEX: Mutex<()> = Mutex::new(());
    let _lock = PRINT_MUTEX.lock().ok();

    let mut output = Vec::new();
    let orig_stdout = std::io::stdout();
    let orig = orig_stdout.lock();

    let prev = std::io::set_print(Some(Box::new(move |args: &Arguments| {
        writeln!(output, "{}", args).unwrap();
    })));

    f();

    std::io::set_print(prev);

    let result = String::from_utf8_lossy(&output).to_string();
    if !result.is_empty() {
        Some(result.trim().to_owned())
    } else {
        None
    }
}

#[test]
fn test_main_prints_message() {
    // Capture stdout with our helper function
    let printed = {
        // Use intercept to capture print
        let old = std::io::set_print(Some(Box::new(|args| {
            LAST_PRINT.with(|s| {
                let msg = format!("{}", args);
                *s.borrow_mut() = Some(msg);
            });
        })));
        appinit::main();
        std::io::set_print(old);
        LAST_PRINT.with(|s| s.borrow().clone())
    };

    assert!(printed.is_some(), "Expected output printed");
    let s = printed.unwrap();
    assert!(s.contains("Call your main application code here"));
}