use std::fs::File;
use std::io::Write;
use std::fs;
use frida_detection::{is_frida_present, test_edge_cases};

fn write_fake_ps(content: &str) {
    let mut file = File::create("/tmp/fake_ps.txt").expect("Failed to create fake ps file");
    file.write_all(content.as_bytes()).expect("Failed to write to fake ps file");
}

#[test]
fn test_is_frida_present_found() {
    write_fake_ps("pid1 bash\npid2 frida-server\npid3 otherproc\n");
    let res = is_frida_present();
    assert_eq!(res, 1);
}

#[test]
fn test_is_frida_present_notfound() {
    write_fake_ps("pid1 bash\npid3 otherproc\n");
    let res = is_frida_present();
    assert_eq!(res, 0);
}

#[test]
fn test_is_frida_present_error() {
    let _ = fs::remove_file("/tmp/fake_ps.txt");
    let res = is_frida_present();
    assert_eq!(res, -1);
}

#[test]
fn test_test_edge_cases() {
    assert_eq!(test_edge_cases(-42), -1);
    assert_eq!(test_edge_cases(0), 0);
    assert_eq!(test_edge_cases(1), 2);
    assert_eq!(test_edge_cases(17), 1);
}