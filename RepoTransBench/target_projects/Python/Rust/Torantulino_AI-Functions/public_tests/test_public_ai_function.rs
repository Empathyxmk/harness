use torantulino_ai_functions::*;
use std::sync::Mutex;
use lazy_static::lazy_static;

// Ensure serial access if test suite runs in parallel
lazy_static! {
    static ref LOCK: Mutex<()> = Mutex::new(());
}

struct DummyChoice {
    content: &'static str,
}
struct DummyResponse {
    choices: Vec<DummyChoice>,
}

#[test]
fn test_public_ai_function_success() {
    let _guard = LOCK.lock().unwrap();
    set_chat_completion_create_mock(|req, messages| {
        assert_eq!(req.model.unwrap_or("gpt-4"), "gpt-4");
        assert!(!messages.is_empty());
        "17".to_string()
    });
    let response = ai_function(
        "def subtract(a, b): return a - b",
        vec!["20", "3"],
        "Subtracts two numbers",
        Some("gpt-4"),
    );
    assert_eq!(response.content, "17");
    reset_chat_completion_create_mock();
}

#[test]
fn test_public_ai_function_custom_model() {
    let _guard = LOCK.lock().unwrap();
    set_chat_completion_create_mock(|req, _messages| {
        assert_eq!(req.model.unwrap(), "gpt-3.5-turbo");
        "15".to_string()
    });
    let response = ai_function(
        "def div(a, b): return a // b",
        vec!["30", "2"],
        "Divide and floor two numbers",
        Some("gpt-3.5-turbo"),
    );
    assert_eq!(response.content, "15");
    reset_chat_completion_create_mock();
}

#[test]
fn test_public_ai_function_no_args() {
    let _guard = LOCK.lock().unwrap();
    set_chat_completion_create_mock(|_req, _messages| {
        "empty args handled".to_string()
    });
    let response = ai_function(
        "def hello(): return 'hello'",
        vec![],
        "No-argument greeting function",
        Some("gpt-4"),
    );
    assert_eq!(response.content, "empty args handled");
    reset_chat_completion_create_mock();
}

#[test]
fn test_public_ai_function_response_structure() {
    let _guard = LOCK.lock().unwrap();

    let mut captured_messages: Option<Vec<Message>> = None;
    set_chat_completion_create_mock(|_req, messages| {
        captured_messages = Some(messages.clone());
        "Y".to_string()
    });

    let response = ai_function(
        "def echo(s): return s",
        vec!["foo"],
        "Echo string argument",
        Some("gpt-4"),
    );
    let messages = response.messages;
    assert_eq!(messages[0].role, "system");
    assert!(messages[0].content.contains("python function"));
    assert_eq!(messages[1].role, "user");
    assert_eq!(messages[1].content, "foo");
    reset_chat_completion_create_mock();
}