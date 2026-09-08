#[test]
fn test_thread_py_importable_custom() {
    // In Rust, importing a module doesn't run code, so this is a no-op
    let _ = crate::thread_mod::run_thread_example as fn();
}

#[test]
fn test_thread_py_main_custom() {
    // Run run_thread_example and check output as in public Python test, but slightly different checks
    use std::io::{self, Write};
    use std::sync::Mutex;
    use std::sync::Arc;

    // Capture stdout
    let output = Arc::new(Mutex::new(Vec::new()));
    let o2 = output.clone();
    let _guard = gag::Redirect::stdout(Box::new(gag::BufferRedirect::new(Box::new(gag::WriteAdapter::new(move |bytes| {
        o2.lock().unwrap().extend_from_slice(bytes);
        Ok(())
    })))).unwrap();

    crate::thread_mod::run_thread_example();

    // Extract and analyze output
    let out_bytes = output.lock().unwrap();
    let out_str = String::from_utf8_lossy(&out_bytes);
    let lines: Vec<_> = out_str.lines().collect();
    assert!(lines.iter().any(|l| l.contains("HammsServer started")));
    // Public: check that the second last line is "stopping" (case insensitive, trim)
    assert!(
        lines.len() >= 2 && lines[lines.len()-2].trim().to_lowercase() == "stopping"
    );
    assert!(
        lines.len() >= 1 && lines[lines.len()-1].contains("HammsServer stopped")
    );
}