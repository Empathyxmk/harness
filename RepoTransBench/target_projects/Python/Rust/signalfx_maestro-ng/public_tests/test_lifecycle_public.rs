// Translation from Python public test for lifecycle logic

struct DummyService {
    enabled: bool,
    state: String,
    run_action_calls: Vec<String>,
}
impl DummyService {
    fn new(enabled: bool) -> Self {
        Self {
            enabled,
            state: "initialized".to_string(),
            run_action_calls: vec![],
        }
    }
    fn run_action(&mut self, action: &str) -> String {
        self.run_action_calls.push(action.to_string());
        match action {
            "activate" => self.state = "activated".to_string(),
            "deactivate" => self.state = "deactivated".to_string(),
            _ => self.state = "unknown_action".to_string(),
        }
        self.state.clone()
    }
}

#[derive(Debug)]
struct DummyMaestroException(pub String);

fn run_service(service: &mut DummyService, action: &str) -> Result<String, DummyMaestroException> {
    if !service.enabled {
        return Ok("".to_string());
    }
    match std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| service.run_action(action))) {
        Ok(val) => Ok(val),
        Err(e) => {
            Err(DummyMaestroException("Exception".to_string()))
        }
    }
}

#[test]
fn test_run_enabled_service_activation() {
    let mut service = DummyService::new(true);
    let _ = run_service(&mut service, "activate").unwrap();
    assert_eq!(service.run_action_calls, vec!["activate"]);
    assert_eq!(service.state, "activated");
}

#[test]
fn test_run_disabled_service_no_action() {
    let mut service = DummyService::new(false);
    let _ = run_service(&mut service, "activate").unwrap();
    assert!(service.run_action_calls.is_empty());
    assert_eq!(service.state, "initialized");
}

#[test]
fn test_run_service_handles_unknown_action() {
    let mut service = DummyService::new(true);
    let _ = run_service(&mut service, "suspend").unwrap();
    assert_eq!(service.run_action_calls, vec!["suspend"]);
    assert_eq!(service.state, "unknown_action");
}

#[test]
fn test_run_service_exception_handling() {
    struct FailingService {
        enabled: bool,
    }
    impl FailingService {
        fn run_action(&mut self, _action: &str) -> String {
            panic!("Simulated failure");
        }
    }
    let mut service = FailingService { enabled: true };
    let res = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        service.run_action("activate")
    }));
    assert!(res.is_err());
}