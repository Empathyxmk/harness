// Only logic and error construction/handling is tested here.

#[derive(Debug)]
struct PyiCloudException(String);

impl std::fmt::Display for PyiCloudException {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl std::error::Error for PyiCloudException {}

#[derive(Debug)]
struct PyiCloudAPIResponseException {
    reason: String,
    code: Option<String>,
    retry: bool,
}

impl std::fmt::Display for PyiCloudAPIResponseException {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let mut s = format!("{}", self.reason);
        if let Some(code) = &self.code {
            s.push_str(&format!(" code: {}", code));
        }
        if self.retry {
            s.push_str(", Retrying...");
        }
        write!(f, "{}", s)
    }
}

impl std::error::Error for PyiCloudAPIResponseException {}

#[derive(Debug)]
struct PyiCloudServiceNotActivatedException(String);
#[derive(Debug)]
struct PyiCloudFailedLoginException(String);
#[derive(Debug)]
struct PyiCloud2SARequiredException(String);
#[derive(Debug)]
struct PyiCloudNoStoredPasswordAvailableException(String);
#[derive(Debug)]
struct PyiCloudNoDevicesException(String);

#[test]
fn test_pyi_cloud_exception() {
    let ex = PyiCloudException("test".to_string());
    assert!(format!("{}", ex).contains("test"));
}

#[test]
fn test_pyi_cloud_api_response_exception_basic() {
    let ex = PyiCloudAPIResponseException { reason: "error reason".to_string(), code: None, retry: false };
    assert!(format!("{}", ex).contains("error reason"));
    assert_eq!(ex.reason, "error reason");
    assert_eq!(ex.code, None);
}

#[test]
fn test_pyi_cloud_api_response_exception_full() {
    let ex = PyiCloudAPIResponseException { reason: "fail".to_string(), code: Some("42".to_string()), retry: true };
    let s = format!("{}", ex);
    assert!(s.contains("fail") && s.contains("42") && s.contains("Retrying"));
    assert_eq!(ex.reason, "fail");
    assert_eq!(ex.code.as_deref(), Some("42"));
}

#[test]
fn test_service_not_activated_exception() {
    let ex = PyiCloudServiceNotActivatedException("reason".to_string());
    assert!(format!("{:?}", ex).contains("reason"));
}

#[test]
fn test_failed_login_exception() {
    let ex = PyiCloudFailedLoginException("login fail".to_string());
    assert!(format!("{:?}", ex).contains("login fail"));
}

#[test]
fn test_2sa_required_exception() {
    let ex = PyiCloud2SARequiredException("email@email.com".to_string());
    assert!(format!("{:?}", ex).contains("email@email.com"));
}

#[test]
fn test_no_stored_password_exception() {
    let ex = PyiCloudNoStoredPasswordAvailableException("no password".to_string());
    assert!(format!("{:?}", ex).contains("no password"));
}

#[test]
fn test_no_devices_exception() {
    let ex = PyiCloudNoDevicesException("no device".to_string());
    assert!(format!("{:?}", ex).contains("no device"));
}