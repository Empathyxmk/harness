// Mock logic for user login/register etc.

struct MockUserManager {
    users: std::collections::HashMap<String, String>,
}
impl MockUserManager {
    fn new() -> Self {
        let mut users = std::collections::HashMap::new();
        users.insert("test@test.com".to_string(), "test".to_string()); // initial test user
        Self { users }
    }

    fn login(&self, username: &str, password: &str) -> Result<&str, usize> {
        match self.users.get(username) {
            Some(pass) if pass == password => Ok("token"),
            _ => Err(4003),
        }
    }
    fn add_user(&mut self, username: &str, password: &str) -> bool {
        self.users.entry(username.to_string()).or_insert(password.to_string());
        true
    }
    fn get_user(&self, username: &str) -> Option<&str> {
        self.users.get(username).map(|_| "nickname")
    }
}

#[test]
fn test_login() {
    let um = MockUserManager::new();
    let result = um.login("test@test.com", "test");
    assert!(result.is_ok());
    assert_eq!(result.unwrap(), "token");
}

#[test]
fn test_error_login() {
    let um = MockUserManager::new();
    let result = um.login("test1@test.com", "t");
    assert!(matches!(result, Err(4003)));
}

#[test]
fn test_get_user() {
    let um = MockUserManager::new();
    let result = um.get_user("test@test.com");
    assert!(result.is_some());
    assert_eq!(result.unwrap(), "nickname");
}