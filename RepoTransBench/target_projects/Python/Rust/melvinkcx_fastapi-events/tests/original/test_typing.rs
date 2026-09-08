use std::collections::HashMap;

#[test]
fn test_event_typing_union_and_aliases() {
    #[derive(Debug, PartialEq, Eq, Hash)]
    enum DummyEnum {
        A,
    }

    type Event<'a> = (&'a str, serde_json::Value);

    // e1: typing.Event = ("test", {"k": 1})
    let e1: (&str, serde_json::Value) = ("test", serde_json::json!({"k": 1}));
    // e2: typing.Event = (DummyEnum.A, "val")
    let e2: (DummyEnum, &str) = (DummyEnum::A, "val");

    // simulate Python's isinstance(e1, tuple)
    assert_eq!(e1.0, "test");
    assert_eq!(e2.1, "val");
    // Scope/Message
    let mut dummy_scope: HashMap<&str, &str> = HashMap::new();
    dummy_scope.insert("type", "http");
    let mut dummy_msg: HashMap<&str, i32> = HashMap::new();
    dummy_msg.insert("a", 1);
    assert_eq!(dummy_scope["type"], "http");
    assert_eq!(dummy_msg["a"], 1);
}

#[test]
fn test_asgiapp_types() {
    // Just check that functions are callable
    fn mock_receive() {}
    fn mock_send(_msg: &str) {}
    fn mock_asgiapp(_scope: &str, _rec: fn(), _snd: fn(&str)) {}

    // All are callable (no actual runtime check needed in Rust, but functions are defined)
    mock_receive();
    mock_send("msg");
    mock_asgiapp("scope", mock_receive, mock_send);
}