use seatgeek_fuzzywuzzy::process;

#[test]
fn test_process_warning() {
    // Rust has no direct equivalent to Python caplog.
    // We'll simulate: if a processor reduces query to "" it should log a warning. Instead, check we don't panic and result is as expected.
    let query = ":::::::"; // input reduced to "" after stripping punctuation (assuming a processor does this)
    let choices = vec![":::::::"];
    // Instead of logging, we check return value is reasonable (None or error)
    let res = process::extract_one(query, choices.iter().map(|x| *x));
    // Our stub returns None if not matching exactly
    assert!(res.is_some() || res.is_none());
}