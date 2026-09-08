use maskerlogger::secrets_in_logs_example;

fn log_sensitive_public() {
    secrets_in_logs_example::log_sensitive();
}

#[test]
fn test_log_sensitive_public_runs() {
    log_sensitive_public();
}