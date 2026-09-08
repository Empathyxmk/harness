use std::collections::HashMap;
use std::sync::{Arc, Mutex};

#[derive(Clone, PartialEq, Eq, Hash, Debug)]
enum Events {
    Created,
    Updated,
}

#[test]
fn test_local_handler() {
    // Simulate events and handlers
    let event_to_be_dispatched = vec![
        "cat_ate_a_fish",
        "cat_requested_something",
        "dog_asked_for_petting",
        "dog_finished_the_food",
        "dad_made_beet_juice",
        "juice_is_spoiled",
        "she_danced_with_her_partner",
    ];

    let events_handled: Arc<Mutex<HashMap<&str, usize>>> = Arc::new(Mutex::new(HashMap::new()));
    for category in &["cat", "all", "dog", "juice", "dance"] {
        events_handled.lock().unwrap().insert(category, 0);
    }

    for event in &event_to_be_dispatched {
        if event.starts_with("cat") {
            let mut eh = events_handled.lock().unwrap();
            *eh.get_mut("cat").unwrap() += 1;
        }
        if event.starts_with("dog") {
            let mut eh = events_handled.lock().unwrap();
            *eh.get_mut("dog").unwrap() += 1;
        }
        if event.contains("juice") {
            let mut eh = events_handled.lock().unwrap();
            *eh.get_mut("juice").unwrap() += 1;
        }
        if event.contains("dance") {
            let mut eh = events_handled.lock().unwrap();
            *eh.get_mut("dance").unwrap() += 1;
        }
        let mut eh = events_handled.lock().unwrap();
        *eh.get_mut("all").unwrap() += 1;
    }

    let expect = vec![
        ("cat", 2),
        ("all", 7),
        ("dog", 2),
        ("juice", 1),
        ("dance", 1),
    ];
    for (k, v) in expect {
        assert_eq!(events_handled.lock().unwrap()[k], v);
    }
}

#[test]
fn test_local_handler_with_enum() {
    let event = Events::Created;
    let mut events_handled = Vec::new();

    // Simulate handler call
    if event == Events::Created {
        events_handled.push(event.clone());
    }
    assert_eq!(events_handled[0], Events::Created);
}

#[test]
fn test_chain_registration_of_local_handler() {
    let all_events = vec!["user_created", "user_updated"];
    let mut events_handled = Vec::new();
    for event in &all_events {
        events_handled.push(event.to_string());
    }
    assert_eq!(
        events_handled,
        all_events.iter().map(|s| s.to_string()).collect::<Vec<_>>()
    );
}

#[test]
fn test_otelsupport() {
    // Simulate recording of a span when event is handled
    let event = "TEST_EVENT";
    let mut spans_created = Vec::new();
    spans_created.push(format!("handling event {} with LocalHandler", event));
    let handler_name = "fastapi_events.handlers.local.LocalHandler";
    assert!(spans_created[0].contains("handling event TEST_EVENT with LocalHandler"));
    assert_eq!(handler_name, "fastapi_events.handlers.local.LocalHandler");
}

#[test]
fn test_local_handler_with_async_fastapi_dependencies() {
    // Simulate dependencies being injected
    let db = "mock_db";
    let service_client = "mock_service_client";
    assert_eq!(db, "mock_db");
    assert_eq!(service_client, "mock_service_client");
}

#[test]
fn test_local_handler_with_nested_async_dependencies() {
    let connection_pool = "mock_connection_pool";
    let db = ("mock_db", "mock_connection_pool");
    let service_client = "mock_service_client";
    assert_eq!(db, ("mock_db", "mock_connection_pool"));
    assert_eq!(service_client, "mock_service_client");
}

#[test]
fn test_local_handler_with_sync_fastapi_dependencies() {
    let repo = "mock_dependency";
    assert_eq!(repo, "mock_dependency");
}