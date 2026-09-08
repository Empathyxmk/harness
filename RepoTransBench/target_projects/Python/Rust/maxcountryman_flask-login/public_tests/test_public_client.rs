#[cfg(test)]
mod tests {
    use crate::test_client::*;

    #[test]
    fn test_flask_login_client_sets_user_id_public() {
        let u = DummyUser::new("U987");
        let client = FlaskLoginClient::new(Some(&u), Some(false));
        assert_eq!(client.sess.get("_user_id").unwrap(), "U987");
        assert_eq!(client.sess.get("_fresh").unwrap(), "false");
    }

    #[test]
    fn test_flask_login_client_no_user_public() {
        let client = FlaskLoginClient::new(None, None);
        assert!(client.sess.get("_user_id").is_none());
        assert!(client.sess.get("_fresh").is_none());
    }
}