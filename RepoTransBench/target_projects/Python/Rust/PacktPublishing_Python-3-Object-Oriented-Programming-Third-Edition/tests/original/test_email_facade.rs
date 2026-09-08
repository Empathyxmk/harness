#[cfg(test)]
mod tests {
    use super::super::super::email_facade::*;

    #[test]
    fn test_send_email_monkeypatch() {
        let mut dummy = DummySMTP::new("host.com");
        dummy.login("user", "pw");
        dummy.sendmail("user@host.com", vec!["dest@host.com".to_string()], "From: user@host.com\nHi\nMessage body");
        assert_eq!(dummy.logged_in, Some(("user".to_string(), "pw".to_string())));
        assert!(dummy.sent);
        assert!(dummy.last_args.as_ref().unwrap().2.contains("From: user@host.com"));
        assert_eq!(dummy.last_args.as_ref().unwrap().1, vec!["dest@host.com".to_string()]);
    }

    #[test]
    fn test_send_email_with_full_address() {
        let mut dummy = DummySMTP::new("host.com");
        dummy.login("auser@domain.com", "pw");
        dummy.sendmail("auser@domain.com", vec!["to@host.com".to_string()], "From: auser@domain.com\nSubj\nBody");
        assert_eq!(dummy.logged_in.as_ref().unwrap().0, "auser@domain.com".to_string());
        assert!(dummy.sent);
        assert!(dummy.last_args.as_ref().unwrap().2.contains("From: auser@domain.com"));
    }

    #[test]
    fn test_get_inbox_monkeypatch() {
        let mut dummy = DummyIMAP4::new("s");
        dummy.login("u", "p");
        dummy.select();
        let (status, ids) = dummy.search();
        assert!(dummy.logged.is_some());
        assert!(dummy.selected);
        assert_eq!(status, "OK".to_string());
        assert!(!ids.is_empty());
    }
}