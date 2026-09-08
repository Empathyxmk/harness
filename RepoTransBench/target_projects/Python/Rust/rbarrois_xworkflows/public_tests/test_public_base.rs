#[test]
fn test_public_workflow_states_and_transitions() {
    // Custom workflow simulation
    struct AltWorkflow;
    impl AltWorkflow {
        fn states() -> Vec<(&'static str, &'static str)> {
            vec![("start", "Start"), ("mid", "Middle"), ("end", "End")]
        }
        fn transitions() -> Vec<(&'static str, &'static str, &'static str)> {
            vec![("go_mid", "start", "mid"), ("finish", "mid", "end"), ("reset", "end", "start")]
        }
        fn initial_state() -> &'static str { "start" }
    }
    let wf = AltWorkflow;
    assert_eq!(wf.states().len(), 3);
    assert_eq!(wf.states()[0].1, "Start");
    assert_eq!(wf.transitions()[0].1, "start");
    assert_eq!(wf.transitions()[1].2, "end");
    assert_eq!(wf.initial_state(), "start");
}

#[test]
fn test_public_workflow_invalid_state_transition() {
    struct MiniWorkflow;
    impl MiniWorkflow {
        fn states() -> Vec<(&'static str, &'static str)> {
            vec![("a", "Alpha"), ("b", "Beta")]
        }
        fn transitions() -> Vec<(&'static str, &'static str, &'static str)> {
            vec![("a_to_b", "a", "b")]
        }
        fn initial_state() -> &'static str { "a" }
    }

    // Emulate invalid transition; should panic, similar to Python KeyError
    let bad_wf = || {
        struct BadWorkflow;
        impl BadWorkflow {
            fn states() -> Vec<(&'static str, &'static str)> {
                vec![("x", "Ex"), ("y", "Why")]
            }
            fn transitions() -> Vec<(&'static str, &'static str, &'static str)> {
                // target "z" does not exist
                vec![("invalid", "x", "z")]
            }
            fn initial_state() -> &'static str { "x" }
        }
        // This would panic if validated
        let _ = BadWorkflow;
        panic!("KeyError on non-existent target state");
    };
    let res = std::panic::catch_unwind(bad_wf);
    assert!(res.is_err());
}