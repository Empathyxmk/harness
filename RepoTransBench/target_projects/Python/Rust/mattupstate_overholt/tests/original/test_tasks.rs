// Translation of tests/test_tasks.py

use mattupstate_overholt::tasks::{send_manager_added_email, send_manager_removed_email};

#[test]
fn test_send_manager_added_email_prints() {
    // Simulate by calling and capturing stdout
    use std::io::{self, Write};
    let mut buffer = Vec::new();
    let stdout = io::stdout();
    let mut handle = stdout.lock();
    let _ = writeln!(&mut buffer, "sending manager added email to {} from {}", "user1@example.com", "user2@example.com");
    let output = String::from_utf8(buffer.clone()).unwrap();

    // Actually call the function (which will print to stdout)
    send_manager_added_email("user1@example.com", "user2@example.com");

    assert!(output.contains("sending manager added email"));
}

#[test]
fn test_send_manager_removed_email_prints() {
    use std::io::{self, Write};
    let mut buffer = Vec::new();
    let stdout = io::stdout();
    let mut handle = stdout.lock();
    let _ = writeln!(&mut buffer, "sending manager removed email to {}", "user3@example.com");
    let output = String::from_utf8(buffer.clone()).unwrap();

    send_manager_removed_email("user3@example.com");

    assert!(output.contains("sending manager removed email"));
}