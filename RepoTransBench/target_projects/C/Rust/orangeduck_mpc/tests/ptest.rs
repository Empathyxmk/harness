//! Rust equivalent of the ptest framework used in the original C code
//! This provides similar macros and functions to the original ptest

use std::panic;

pub fn assert_str_eq(fst: &str, snd: &str, file: &str, line: u32) {
    if fst != snd {
        panic!("strcmp( {}, {} ) == 0 ({}, line {})", fst, snd, file, line);
    }
}

#[macro_export]
macro_rules! pt_assert {
    ($expr:expr) => {
        assert!($expr);
    };
}

#[macro_export]
macro_rules! pt_assert_str_eq {
    ($fst:expr, $snd:expr) => {
        assert_eq!($fst, $snd);
    };
}

// Helper function to run a test and check if it panics
pub fn run_test<F>(test_fn: F) -> bool
where
    F: FnOnce() + panic::UnwindSafe,
{
    let result = panic::catch_unwind(test_fn);
    result.is_ok()
}

// Helper to print test results
pub fn print_test_results(passed: usize, failed: usize) {
    println!("\n  +---------------------------------------------------+");
    println!("  |                      Summary                      |");
    println!("  +---------++------------+-------------+-------------+");
    println!("  | Tests   || Total {:4} | Passed {:4} | Failed {:4} |", 
        passed + failed, passed, failed);
    println!("  +---------++------------+-------------+-------------+");
    println!("");
}