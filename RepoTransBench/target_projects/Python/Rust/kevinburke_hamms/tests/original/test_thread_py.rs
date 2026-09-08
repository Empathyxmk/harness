use std::sync::{Arc, Mutex};

#[test]
fn test_thread_py_importable() {
    // Simulating "import thread" in Rust - just ensure src/thread.rs exists and is usable
    // This is a no-op test, as Rust does not run code on module import
    // The point is to check importing does not panic
    let _ = crate::thread_mod::run_thread_example as fn();
}

#[test]
fn test_thread_py_main_captures_output() {
    // Simulate the test: running run_thread_example() and check output
    use std::io::{self, Write};
    use std::sync::Mutex;

    // Capture stdout
    let output = Arc::new(Mutex::new(Vec::new()));
    let o2 = output.clone();
    let _guard = gag::Redirect::stdout(Box::new(gag::BufferRedirect::new(Box::new(gag::WriteAdapter::new(move |bytes| {
        o2.lock().unwrap().extend_from_slice(bytes);
        Ok(())
    })))).unwrap();

    crate::thread_mod::run_thread_example();

    // Extract and validate output
    let out_bytes = output.lock().unwrap();
    let out_str = String::from_utf8_lossy(&out_bytes);
    assert!(out_str.contains("HammsServer started"));
    assert!(out_str.contains("stopping"));
    assert!(out_str.contains("HammsServer stopped"));
}