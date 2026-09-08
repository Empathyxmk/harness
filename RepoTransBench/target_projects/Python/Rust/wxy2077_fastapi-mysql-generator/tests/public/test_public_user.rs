use std::collections::HashMap;

struct PublicUserManager {
    users: HashMap<String, String>,
    nicknames: HashMap<String, String>,
}
impl PublicUserManager {
    fn new() -> Self {
        let mut users = HashMap::new();
        let mut nicknames = HashMap::new();
        Self { users, nicknames }
    }

    fn register(&mut self, username: &str, password: &str, nick_name: &str) -> (&'static str, usize) {
        self.users.insert(username.to_string(), password.to_string());
        self.nicknames.insert(username.to_string(), nick_name.to_string());
        ("registered", 200)
    }

    fn query(&self, username: &str) -> Vec<String> {
        self.users.get(username).map(|_| vec![username.to_string()]).unwrap_or_else(Vec::new)
    }

    fn login(&self, username: &str, password: &str) -> Result<&'static str, usize> {
        match self.users.get(username) {
            Some(pass) if pass == password => Ok("access_token"),
            _ => Err(4003),
        }
    }

    fn update_password(&mut self, username: &str, old_password: &str, new_password: &str) -> usize {
        match self.users.get_mut(username) {
            Some(pass) if *pass == old_password => {
                *pass = new_password.to_string();
                200
            },
            _ => 4003,
        }
    }

    fn delete(&mut self, username: &str) -> usize {
        self.users.remove(username).map(|_| 200).unwrap_or(4003)
    }
}

#[test]
fn test_create_user_public() {
    let mut um = PublicUserManager::new();
    let username = "publicuser42";
    let password = "publicpassword42";
    let (msg, code) = um.register(username, password, "PublicNick42");
    assert_eq!(code, 200);
    assert_eq!(msg, "registered");
    assert_eq!(um.users.get(username).unwrap(), password);
}

#[test]
fn test_search_user_public() {
    let mut um = PublicUserManager::new();
    let username = "publicuser42";
    um.register(username, "publicpassword42", "PublicNick42");
    let data = um.query(username);
    assert!(!data.is_empty());
    assert!(data.iter().any(|u| u == username));
}

#[test]
fn test_user_login_public() {
    let mut um = PublicUserManager::new();
    let username = "publicuser42";
    let password = "publicpassword42";
    um.register(username, password, "PublicNick42");
    let result = um.login(username, password);
    assert!(result.is_ok());
    assert_eq!(result.unwrap(), "access_token");
}

#[test]
fn test_update_password_public() {
    let mut um = PublicUserManager::new();
    let username = "publicuser42";
    let old_password = "publicpassword42";
    let new_password = "publicpassword_updated";
    um.register(username, old_password, "PublicNick42");
    let code = um.update_password(username, old_password, new_password);
    assert_eq!(code, 200);
    assert_eq!(um.users.get(username).unwrap(), new_password);
}

#[test]
fn test_delete_user_public() {
    let mut um = PublicUserManager::new();
    let username = "publicuser42";
    um.register(username, "publicpassword42", "PublicNick42");
    let code = um.delete(username);
    assert_eq!(code, 200);
    assert!(um.users.get(username).is_none());
}