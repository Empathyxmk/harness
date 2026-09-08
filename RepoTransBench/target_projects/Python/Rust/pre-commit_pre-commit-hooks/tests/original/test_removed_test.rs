// Rust translation of tests/removed_test.py

#[test]
fn test_always_fails() {
    let result = std::panic::catch_unwind(|| {
        main_removed(&[
            "autopep8-wrapper", "autopep8",
            "https://github.com/pre-commit/mirrors-autopep8",
            "--foo", "bar",
        ]);
    });
    // Check that it panicked (corresponds to SystemExit)
    assert!(result.is_err());
}

fn main_removed(_args: &[&str]) {
    panic!("`autopep8-wrapper` has been removed -- use `autopep8` from https://github.com/pre-commit/mirrors-autopep8");
}