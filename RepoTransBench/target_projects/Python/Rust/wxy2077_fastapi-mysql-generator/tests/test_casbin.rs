struct MockCasbin {
    // user: ("authority_id", "path", "method") => status
    is_superuser: bool,
}
impl MockCasbin {
    fn new(is_superuser: bool) -> Self {
        Self { is_superuser }
    }

    fn add_auth(&self) -> usize {
        if self.is_superuser { 200 } else { 4003 }
    }
    fn del_auth(&self) -> usize {
        if self.is_superuser { 200 } else { 4003 }
    }
}

#[test]
fn test_ordinary_add_auth() {
    let c = MockCasbin::new(false);
    assert_eq!(c.add_auth(), 4003);
}

#[test]
fn test_ordinary_del_auth() {
    let c = MockCasbin::new(false);
    assert_eq!(c.del_auth(), 4003);
}

#[test]
fn test_admin_add_auth() {
    let c = MockCasbin::new(true);
    assert_eq!(c.add_auth(), 200);
}

#[test]
fn test_admin_del_auth() {
    let c = MockCasbin::new(true);
    assert_eq!(c.del_auth(), 200);
}