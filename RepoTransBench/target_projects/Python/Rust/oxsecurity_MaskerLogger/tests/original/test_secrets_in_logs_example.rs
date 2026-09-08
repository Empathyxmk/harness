use maskerlogger::secrets_in_logs_example;

#[test]
fn test_import_and_main() {
    secrets_in_logs_example::main();
}

#[test]
fn test_log_sensitive_runs() {
    secrets_in_logs_example::log_sensitive();
}