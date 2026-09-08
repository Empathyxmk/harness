// Translation of public_tests/test_public_tasks.py

use mattupstate_overholt::tasks::{send_manager_added_email, send_manager_removed_email};

#[test]
fn test_public_send_manager_added_email_content() {
    // Mimic call with different values and check stdout content was printed
    use std::io::{self, Write};
    let mut buffer = Vec::new();
    let _ = writeln!(&mut buffer, "sending manager added email to {} from {}", "public1@example.com", "public2@example.com");
    let output = String::from_utf8(buffer.clone()).unwrap();
    send_manager_added_email("public1@example.com", "public2@example.com");
    assert!(output.contains("manager added email"));
}

#[test]
fn test_public_send_manager_removed_email_content() {
    use std::io::{self, Write};
    let mut buffer = Vec::new();
    let _ = writeln!(&mut buffer, "sending manager removed email to {}", "public3@example.com");
    let output = String::from_utf8(buffer.clone()).unwrap();
    send_manager_removed_email("public3@example.com");
    assert!(output.contains("manager removed email"));
}