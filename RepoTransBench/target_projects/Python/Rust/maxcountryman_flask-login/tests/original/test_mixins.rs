#[cfg(test)]
mod tests {
    use crate::mixins::*;

    #[test]
    fn test_user_mixin_is_active() {
        let user = UserMixin::new(1);
        assert!(user.is_active());
    }
    #[test]
    fn test_user_mixin_is_authenticated() {
        let user = UserMixin::new(2);
        assert!(user.is_authenticated());
    }
    #[test]
    fn test_user_mixin_is_anonymous() {
        let user = UserMixin::new(3);
        assert!(!user.is_anonymous());
    }
    #[test]
    fn test_user_mixin_get_id_returns_str() {
        let user = UserMixin::new(123);
        assert_eq!(user.get_id().unwrap(), "123");
        let user2 = UserMixin::new("abc");
        assert_eq!(user2.get_id().unwrap(), "abc");
    }
    #[test]
    fn test_user_mixin_get_id_attribute_error() {
        let mut user = UserMixin::new(1);
        user.id = None;
        let res = user.get_id();
        assert_eq!(res, Err("NotImplementedError"));
    }
    #[test]
    fn test_user_mixin_eq_true() {
        let user1 = UserMixin::new(9);
        let user2 = UserMixin::new(9);
        assert_eq!(user1, user2);
    }
    #[test]
    fn test_user_mixin_eq_false() {
        let user1 = UserMixin::new(1);
        let user2 = UserMixin::new(2);
        assert_ne!(user1, user2);
    }
    #[test]
    fn test_user_mixin_eq_type() {
        let user = UserMixin::new(1);
        let obj: &dyn std::any::Any = &();
        // UserMixin partialeq dyn Any always returns false
        assert_eq!(user == obj, false);
    }
    #[test]
    fn test_user_mixin_ne_type() {
        let user = UserMixin::new(1);
        let obj: &dyn std::any::Any = &();
        assert_eq!(user != obj, true);
    }
    #[test]
    fn test_user_mixin_hash() {
        let user = UserMixin::new(1);
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        let mut hasher = DefaultHasher::new();
        user.hash(&mut hasher);
        let _ = hasher.finish();
    }
    #[test]
    fn test_anonymous_user_mixin_properties() {
        let anon = AnonymousUserMixin;
        assert!(!anon.is_active());
        assert!(!anon.is_authenticated());
        assert!(anon.is_anonymous());
    }
    #[test]
    fn test_anonymous_user_mixin_get_id() {
        let anon = AnonymousUserMixin;
        assert_eq!(anon.get_id(), None);
    }
}