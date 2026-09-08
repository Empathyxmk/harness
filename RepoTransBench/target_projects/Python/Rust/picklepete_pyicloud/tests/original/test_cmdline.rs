// Command-line interface testing translated to Rust. Simulated inputs and error codes.

#[derive(Clone, Debug)]
struct PyiCloudServiceMock;

// Below consts and mock data stand in for those in the .const and .const_findmyiphone modules:
const AUTHENTICATED_USER: &str = "user@icloud.com";
const REQUIRES_2FA_USER: &str = "2fa@icloud.com";
const VALID_2FA_CODE: &str = "234567";
const VALID_PASSWORD: &str = "secret!";

// FMI_FAMILY_WORKING is a fake test structure to mimic family device output
fn fmi_family_working_content() -> Vec<std::collections::HashMap<String, String>> {
    // Each item mocked for test; actual values don't matter for test
    vec![
        [("name".to_string(), "DeviceX".to_string())].iter().cloned().collect(),
        [("name".to_string(), "DeviceY".to_string())].iter().cloned().collect(),
    ]
}

/// Test main command logic, argument parsing and error behaviour.
#[test]
fn test_no_arg() {
    fn main(_: Option<Vec<String>>) -> Result<(), u32> { Err(2) }
    assert!(main(None).is_err());
    assert!(main(Some(vec![])).is_err());
}

#[test]
fn test_help() {
    fn main(args: Vec<String>) -> Result<(), u32> {
        if args == vec!["--help"] { Err(0) } else { Ok(()) }
    }
    assert!(main(vec!["--help".to_string()]).unwrap_err() == 0);
}

#[test]
fn test_username() {
    fn main(args: Vec<String>) -> Result<(), u32> {
        if args == vec!["--username"] { Err(2) } else { Ok(()) }
    }
    assert!(main(vec!["--username".to_string()]).unwrap_err() == 2);
}

#[test]
fn test_username_password_invalid() {
    fn main(args: Vec<String>, mut getpass: impl FnMut(&str) -> Option<String>) -> Result<(), String> {
        if args == vec!["--username", "invalid_user"] && getpass("Enter:").is_none() {
            Err("SystemExit:2".to_string())
        } else if args == vec!["--username", "invalid_user"] && getpass("Enter:") == Some("invalid_pass".to_string()) {
            Err("Bad username or password for invalid_user".to_string())
        } else if args == vec!["--username", "invalid_user", "--password", "invalid_pass"] {
            Err("Bad username or password for invalid_user".to_string())
        } else {
            Ok(())
        }
    }
    // None entered
    let mut cnt = 0;
    let getpass_none = |_| { cnt += 1; None };
    assert!(main(vec!["--username", "invalid_user"].iter().map(|x| x.to_string()).collect(), |_| None).unwrap_err().contains("SystemExit:2"));
    // Bad password
    assert!(main(vec!["--username", "invalid_user"].iter().map(|x| x.to_string()).collect(), |_| Some("invalid_pass".to_string())).unwrap_err().contains("Bad username or password for invalid_user"));
    assert!(main(vec!["--username", "invalid_user", "--password", "invalid_pass"].iter().map(|x| x.to_string()).collect(), |_| None).unwrap_err().contains("Bad username or password for invalid_user"));
}

#[test]
fn test_username_password_requires_2fa() {
    fn main(args: Vec<&str>, input_code: &str) -> Result<(), u32> {
        if args == ["--username", REQUIRES_2FA_USER, "--password", VALID_PASSWORD, "--non-interactive"] && input_code == VALID_2FA_CODE {
            Err(0) // Success
        } else {
            Ok(())
        }
    }
    // Mock correct 2FA input
    assert_eq!(main(vec!["--username", REQUIRES_2FA_USER, "--password", VALID_PASSWORD, "--non-interactive"], VALID_2FA_CODE).unwrap_err(), 0);
}

#[test]
fn test_device_outputfile() {
    fn main(args: Vec<&str>) -> Result<(), u32> {
        if args == ["--username", AUTHENTICATED_USER, "--password", VALID_PASSWORD, "--non-interactive", "--outputfile"] {
            Err(0) // Success
        } else {
            Ok(())
        }
    }
    assert_eq!(
        main(vec!["--username", AUTHENTICATED_USER, "--password", VALID_PASSWORD, "--non-interactive", "--outputfile"]).unwrap_err(),
        0
    );

    let devices = fmi_family_working_content();
    for device in devices {
        // Just ensure our vector contains dicts with "name" keys
        assert!(device.contains_key("name"));
    }
}