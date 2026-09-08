use std::collections::HashMap;

#[test]
fn test_gp_group_vars() {
    let gp = "grandparent";
    let gvars: HashMap<&str, &str> = [("gp_not_overridden", "gp")].iter().cloned().collect();
    assert_eq!(gvars.keys().cloned().collect::<Vec<&str>>(), vec!["gp_not_overridden"]);
    assert_eq!(gvars["gp_not_overridden"], "gp");
}

#[test]
fn test_parent_group_vars() {
    let parent = "parent";
    let pvars: HashMap<&str, &str> = [
        ("parent_not_overridden", "parent"),
        ("gp_overridden_in_parent", "gp"),
    ].iter().cloned().collect();
    assert_eq!(
        pvars.keys().cloned().collect::<Vec<&str>>(),
        vec!["parent_not_overridden", "gp_overridden_in_parent"]
    );
    assert_eq!(pvars["parent_not_overridden"], "parent");
}

#[test]
fn test_host_vars() {
    let hvars: HashMap<&str, &str> = [
        ("gp_overridden_in_child", "child"),
        ("parent_overridden_in_child", "child"),
        ("child_only", "child"),
    ].iter().cloned().collect();
    assert_eq!(hvars["gp_overridden_in_child"], "child");
    assert_eq!(hvars["parent_overridden_in_child"], "child");
    assert_eq!(hvars["child_only"], "child");
}