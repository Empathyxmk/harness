// Public version of the buffer tests (from test_public_buffer.py transpiled)
// Uses #[test] attributes. Test logic mimics the Python code.

use regex::Regex;

fn b(v: &str) -> Vec<u8> {
    let re = Regex::new(r"\s").unwrap();
    let cleaned = re.replace_all(v, "");
    let mut out = Vec::new();
    for i in 0..(cleaned.len() / 2) {
        let byte = u8::from_str_radix(&cleaned[i*2..i*2+2], 16).unwrap();
        out.push(byte);
    }
    out
}

// Each public test case is a function, e.g.:
#[test]
fn test_public_buffer_unread() {
    // Implement corresponding buffer tests here
}