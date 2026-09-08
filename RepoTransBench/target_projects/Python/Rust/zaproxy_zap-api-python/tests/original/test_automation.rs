use zaproxy_zap_api_rust::zapv2::automation::{DummyZapAutomation, Automation};

fn setup_automation<'a>() -> Automation<'a> {
    let mut zap = Box::new(DummyZapAutomation::new());
    Automation::new(Box::leak(zap))
}

#[test]
fn test_plan_progress() {
    let mut automation = setup_automation();
    let v = automation.plan_progress("myplan");
    assert_eq!(v, serde_json::json!({ "value": "dummy" }));
}

#[test]
fn test_run_plan() {
    let mut automation = setup_automation();
    let v = automation.run_plan("/tmp/file.yaml");
    assert_eq!(v, "dummy");
}

#[test]
fn test_end_delay_job() {
    let mut automation = setup_automation();
    let v = automation.end_delay_job();
    assert_eq!(v, "dummy");
}