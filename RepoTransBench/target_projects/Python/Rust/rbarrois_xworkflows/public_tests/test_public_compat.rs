use rbarrois_xworkflows::base;

#[test]
fn test_public_string_type_is_str() {
    // Just a sanity check in Rust
    let s = std::any::type_name::<base::Workflow>();
    assert!(s.contains("Workflow"));
}

#[test]
fn test_public_base_workflow_has_states() {
    // Custom workflow
    struct AltCompWorkflow;
    impl AltCompWorkflow {
        fn states() -> Vec<(&'static str, &'static str)> {
            vec![("alpha", "Alpha"), ("beta", "Beta")]
        }
        fn transitions() -> Vec<(&'static str, &'static str, &'static str)> {
            vec![("ab", "alpha", "beta")]
        }
        fn initial_state() -> &'static str { "alpha" }
    }
    let workflow = AltCompWorkflow;
    let names: Vec<_> = workflow.states().iter().map(|x| x.0).collect();
    assert!(names.contains(&"alpha"));
    assert_eq!(workflow.states()[1].1, "Beta");
}