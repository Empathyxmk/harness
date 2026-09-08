use torantulino_ai_functions::*;
use std::sync::Mutex;
use lazy_static::lazy_static;

// Helper to safely capture "monkeypatching"/global override state during tests.
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
fn test_ai_function_success() {
    let _guard = LOCK.lock().unwrap();
    set_chat_completion_create_mock(|req, messages| {
        assert_eq!(req.model.unwrap_or("gpt-4"), "gpt-4");
        assert!(!messages.is_empty());
        assert_eq!(messages[0].role, "system");
        "42".to_string()
    });
    let response = ai_function(
        "def add(a, b): return a + b",
        vec!["2", "40"],
        "Adds two numbers",
        Some("gpt-4"),
    );
    assert_eq!(response.content, "42");
    reset_chat_completion_create_mock();
}

#[test]
fn test_ai_function_custom_model() {
    let _guard = LOCK.lock().unwrap();
    set_chat_completion_create_mock(|req, _messages| {
        assert_eq!(req.model.unwrap(), "gpt-3.5-turbo");
        "7".to_string()
    });
    let response = ai_function(
        "def mul(a, b): return a * b",
        vec!["3", "4"],
        "Multiply two numbers",
        Some("gpt-3.5-turbo"),
    );
    assert_eq!(response.content, "7");
    reset_chat_completion_create_mock();
}

#[test]
fn test_ai_function_no_args() {
    let _guard = LOCK.lock().unwrap();
    set_chat_completion_create_mock(|_req, _messages| {
        "no args".to_string()
    });
    let response = ai_function(
        "def f(): return None",
        vec![],
        "No-argument function",
        Some("gpt-4"),
    );
    assert_eq!(response.content, "no args");
    reset_chat_completion_create_mock();
}

#[test]
fn test_ai_function_response_structure() {
    let _guard = LOCK.lock().unwrap();

    let mut captured_messages = None;
    set_chat_completion_create_mock(|_req, messages| {
        captured_messages = Some(messages.clone());
        "X".to_string()
    });

    let response = ai_function(
        "def f(x): return x",
        vec!["7"],
        "Echo integer",
        Some("gpt-4"),
    );
    let messages = response.messages;

    assert_eq!(messages[0].role, "system");
    assert!(messages[0].content.contains("python function"));
    assert_eq!(messages[1].role, "user");
    assert_eq!(messages[1].content, "7");
    reset_chat_completion_create_mock();
}