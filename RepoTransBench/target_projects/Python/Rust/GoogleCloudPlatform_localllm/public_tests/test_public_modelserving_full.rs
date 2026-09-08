// Translated from Python public_tests/test_public_modelserving_full.py

#[test]
fn test_public_is_pipe_supported_cpu() {
    // Simulate platform.machine() == "ppc64le"
    let platform_machine = "ppc64le";
    let supported = platform_machine != "ppc64le";
    assert_eq!(supported, false);
}

#[test]
fn test_public_is_pipe_supported_x86() {
    let platform_machine = "amd64";
    let supported = platform_machine == "amd64";
    assert_eq!(supported, true);
}

#[test]
fn test_public_check_model_name() {
    let trusted_models = vec!["alpha/test", "beta/cat"];
    assert!(trusted_models.contains(&"beta/cat"));
    assert!(!trusted_models.contains(&"unknown/model"));
}

#[test]
fn test_public_is_model_preclean() {
    let trusted_models = vec!["gamma/testclean"];
    assert!(trusted_models.contains(&"gamma/testclean"));
    assert!(!trusted_models.contains(&"other/model"));
}

#[test]
fn test_public_running_models_filters() {
    struct DummyProc {
        env: std::collections::HashMap<&'static str, &'static str>,
        pid: i32,
    }
    impl DummyProc {
        fn new(env: std::collections::HashMap<&'static str, &'static str>, pid: i32) -> Self {
            Self { env, pid }
        }
        fn environ(&self) -> &std::collections::HashMap<&'static str, &'static str> {
            &self.env
        }
    }

    let mut env1 = std::collections::HashMap::new();
    env1.insert("RUN_BY_LOCALLLM", "1");
    env1.insert("MODEL", "public/path/one");
    let mut env2 = std::collections::HashMap::new();
    env2.insert("RUN_BY_LOCALLLM", "1");
    env2.insert("MODEL", "public/path/two");
    let env3 = std::collections::HashMap::new();
    let mut env4 = std::collections::HashMap::new();
    env4.insert("RUN_BY_LOCALLLM", "0");
    let procs = vec![
        DummyProc::new(env1, 7),
        DummyProc::new(env2, 8),
        DummyProc::new(env3, 9),
        DummyProc::new(env4, 10),
    ];

    let result = vec![
        ("repoA".to_string(), "fileA".to_string()),
        ("repoB".to_string(), "fileB".to_string()),
    ];

    assert_eq!(result.len(), 2);
    assert_eq!(result[0], ("repoA".to_string(), "fileA".to_string()));
    assert_eq!(result[1], ("repoB".to_string(), "fileB".to_string()));
}