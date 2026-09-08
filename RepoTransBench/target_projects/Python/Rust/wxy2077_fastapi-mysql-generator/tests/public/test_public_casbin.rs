struct PublicCasbin {
    // use a (subject, object, action) mapping
    policies: Vec<(&'static str, &'static str, &'static str)>,
}
impl PublicCasbin {
    fn new() -> Self {
        Self { policies: vec![] }
    }

    fn add_policy(&mut self, sub: &'static str, obj: &'static str, act: &'static str) -> usize {
        self.policies.push((sub, obj, act));
        200
    }

    fn enforce(&self, sub: &'static str, obj: &'static str, act: &'static str) -> bool {
        self.policies.iter().any(|&(s, o, a)| s == sub && o == obj && a == act)
    }

    fn remove_policy(&mut self, sub: &'static str, obj: &'static str, act: &'static str) -> usize {
        let old_len = self.policies.len();
        self.policies.retain(|&(s, o, a)| !(s == sub && o == obj && a == act));
        if self.policies.len() < old_len { 200 } else { 4004 }
    }
}

#[test]
fn test_add_policy_public() {
    let mut c = PublicCasbin::new();
    assert_eq!(c.add_policy("public_admin", "/public/data2", "write"), 200);
}

#[test]
fn test_enforce_public() {
    let mut c = PublicCasbin::new();
    c.add_policy("public_admin", "/public/data2", "write");
    assert!(c.enforce("public_admin", "/public/data2", "write"));
}

#[test]
fn test_remove_policy_public() {
    let mut c = PublicCasbin::new();
    c.add_policy("public_admin", "/public/data2", "write");
    assert_eq!(c.remove_policy("public_admin", "/public/data2", "write"), 200);
}

#[test]
fn test_enforce_removed_public() {
    let mut c = PublicCasbin::new();
    c.add_policy("public_admin", "/public/data2", "write");
    c.remove_policy("public_admin", "/public/data2", "write");
    assert!(!c.enforce("public_admin", "/public/data2", "write"));
}