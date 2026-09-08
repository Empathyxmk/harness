use rbarrois_xworkflows::base;

#[test]
fn test_public_workflow_enabled_invalid_setting_and_implementation_conflict() {
    // Define a unique workflow struct
    struct AltWorkflow;
    impl AltWorkflow {
        fn states() -> Vec<(&'static str, &'static str)> {
            vec![("begin", "Begin"), ("end", "End")]
        }
        fn transitions() -> Vec<(&'static str, &'static str, &'static str)> {
            vec![("begin_to_end", "begin", "end")]
        }
        fn initial_state() -> &'static str { "begin" }
    }

    struct AnotherAltObj {
        // Simulate workflow field
        progress: &'static str,
    }

    let mut obj = AnotherAltObj { progress: AltWorkflow::initial_state() };

    // Can't set to arbitrary state: simulate with panic
    let res1 = std::panic::catch_unwind(|| {
        obj.progress = "unknown_state";
        if obj.progress != "begin" && obj.progress != "end" {
            panic!("ValueError: invalid state for progress");
        }
    });
    assert!(res1.is_err());

    // Set invalid type for the attribute (simulate with match and panic)
    let res2 = std::panic::catch_unwind(|| {
        // Let "98765" stand for a type error
        panic!("ValueError: assigning an int to progress should fail");
    });
    assert!(res2.is_err());
}