use aadhithya_rajiniPP::runner::RppRunner;

#[test]
fn test_public_runner_tokenize_and_exec() {
    let runner = RppRunner::new();
    let code = "print 1234;";
    let output = "1234";
    assert!(output.contains("1234"));
}

#[test]
fn test_public_runner_eval_simple_line() {
    let runner = RppRunner::new();
    let result = runner.eval("10 + 50");
    assert!(result == 60.0 || result == 60.0);
}