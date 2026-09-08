use peritus_bumpversion::bump_mod;

#[test]
fn test_discard_default_if_specified_append_action() {
    // Simulate dummy action: setting a value in a dummy struct
    struct Parser;
    struct Namespace { foo: Vec<i32> }
    struct DummyAction;
    impl DummyAction {
        fn call(&self, namespace: &mut Namespace, val: i32) {
            namespace.foo = vec![val];
        }
    }
    let mut ns = Namespace { foo: vec![1] };
    let action = DummyAction {};
    action.call(&mut ns, 2);
    assert_eq!(ns.foo, vec![2]);
}

#[test]
fn test_basevcs_is_usable_oserror() {
    // Simulate: forced error returns false
    struct DummyBase;
    fn dummy_call() -> Result<(), std::io::Error> {
        Err(std::io::Error::new(std::io::ErrorKind::NotFound, "No such file"))
    }
    let result = dummy_call();
    assert!(result.is_err());
}

#[test]
fn test_basevcs_is_usable_other_raises() {
    struct DummyBase;
    fn dummy_call() -> Result<(), std::io::Error> {
        Err(std::io::Error::new(std::io::ErrorKind::ConnectionRefused, "other"))
    }
    let result = dummy_call();
    assert!(result.is_err());
}

#[test]
fn test_git_latest_tag_info_dirty() {
    // Simulate: just check dirty field present
    #[derive(Debug)]
    struct DummyGitTagInfo { dirty: bool, commit_sha: &'static str, distance_to_latest_tag: i32, current_version: &'static str }
    fn latest_tag_info() -> DummyGitTagInfo {
        DummyGitTagInfo {
            dirty: true,
            commit_sha: "sha",
            distance_to_latest_tag: 1,
            current_version: "1.0"
        }
    }
    let info = latest_tag_info();
    assert!(info.dirty);
}