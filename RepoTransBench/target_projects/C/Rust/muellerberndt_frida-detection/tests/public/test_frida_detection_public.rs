use std::fs::File;
use std::io::Write;
use std::fs;
use frida_detection::{is_frida_present, test_edge_cases};

fn write_fake_ps(content: &str) {
    let mut file = File::create("/tmp/fake_ps.txt").expect("Unable to open /tmp/fake_ps.txt for writing");
    file.write_all(content.as_bytes()).expect("Failed to write to fake ps file");
}

#[test]
fn test_detect_frida_absent_with_other_processes() {
    write_fake_ps("myapp\nsshd\nbash\nvpnclient\n");
    let result = is_frida_present();
    assert_eq!(result, 0);
}

#[test]
fn test_detect_frida_present_amid_noise() {
    write_fake_ps("procX\nprocY\nfrida-server-something\nprocZ\n");
    let result = is_frida_present();
    assert_eq!(result, 1);
}

#[test]
fn test_detect_frida_present_exact() {
    write_fake_ps("procA\nfrida-server\nprocB\n");
    let result = is_frida_present();
    assert_eq!(result, 1);
}

#[test]
fn test_detect_frida_error_open() {
    let _ = fs::remove_file("/tmp/fake_ps.txt");
    let result = is_frida_present();
    assert_eq!(result, -1);
}

#[test]
fn test_edge_cases_public() {
    assert_eq!(test_edge_cases(-15), -1);
    assert_eq!(test_edge_cases(7), 1);
    assert_eq!(test_edge_cases(10), 1);
    assert_eq!(test_edge_cases(0), 0);
    assert_eq!(test_edge_cases(1), 2);
}