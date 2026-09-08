use rvrsh3ll_bof_collection::go_registry_persistence;

#[test]
fn test_install_arg() {
    let arg = b"Install";
    let result = go_registry_persistence(arg);
    assert!(result != 0, "InstallPersistence should trigger");
}

#[test]
fn test_remove_arg() {
    let arg = b"Remove";
    let result = go_registry_persistence(arg);
    assert!(result != 0, "RemovePersistence should trigger");
}

#[test]
fn test_other_arg() {
    let arg = b"SomethingElse";
    let result = go_registry_persistence(arg);
    assert!(result == 0, "Should do nothing special for random arg");
}