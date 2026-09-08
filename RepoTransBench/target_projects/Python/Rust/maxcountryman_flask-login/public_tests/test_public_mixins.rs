#[cfg(test)]
mod tests {
    use crate::mixins::*;

    #[test]
    fn test_user_mixin_is_active_public() {
        let user = UserMixin::new(100);
        assert!(user.is_active());
    }

    #[test]
    fn test_user_mixin_is_authenticated_public() {
        let user = UserMixin::new(200);
        assert!(user.is_authenticated());
    }

    #[test]
    fn test_user_mixin_is_anonymous_public() {
        let user = UserMixin::new(300);
        assert!(!user.is_anonymous());
    }

    #[test]
    fn test_user_mixin_get_id_returns_str_public() {
        let user = UserMixin::new(456);
        assert_eq!(user.get_id().unwrap(), "456");
        let user2 = UserMixin::new("xyz");
        assert_eq!(user2.get_id().unwrap(), "xyz");
    }

    #[test]
    fn test_user_mixin_get_id_attribute_error_public() {
        let mut user = UserMixin::new(10);
        user.id = None;
        let res = user.get_id();
        assert_eq!(res, Err("NotImplementedError"));
    }

    #[test]
    fn test_user_mixin_eq_true_public() {
        let user1 = UserMixin::new(55);
        let user2 = UserMixin::new(55);
        assert_eq!(user1, user2);
    }

    #[test]
    fn test_user_mixin_eq_false_public() {
        let user1 = UserMixin::new(11);
        let user2 = UserMixin::new(12);
        assert_ne!(user1, user2);
    }

    #[test]
    fn test_user_mixin_eq_type_public() {
        let user = UserMixin::new(222);
        let obj: &dyn std::any::Any = &();
        assert_eq!(user == obj, false);
    }

    #[test]
    fn test_user_mixin_ne_type_public() {
        let user = UserMixin::new(1234);
        let obj: &dyn std::any::Any = &();
        assert_eq!(user != obj, true);
    }

    #[test]
    fn test_user_mixin_hash_public() {
        let user = UserMixin::new(42);
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        let mut hasher = DefaultHasher::new();
        user.hash(&mut hasher);
        let _ = hasher.finish();
    }

    #[test]
    fn test_anonymous_user_mixin_properties_public() {
        let anon = AnonymousUserMixin;
        assert!(!anon.is_active());
        assert!(!anon.is_authenticated());
        assert!(anon.is_anonymous());
    }

    #[test]
    fn test_anonymous_user_mixin_get_id_public() {
        let anon = AnonymousUserMixin;
        assert_eq!(anon.get_id(), None);
    }
}