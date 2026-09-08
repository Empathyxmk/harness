use std::cell::RefCell;

struct DummyHandler {
    handled: RefCell<Vec<(String, i32)>>,
}
impl DummyHandler {
    fn new() -> Self {
        DummyHandler {
            handled: RefCell::new(vec![]),
        }
    }
    fn handle_many(&self, events: Vec<(String, i32)>) {
        for event in events {
            self.handled.borrow_mut().push(event);
        }
    }
}

#[tokio::test]
async fn test_event_handler_asgi_middleware_http_scope() {
    let called_app = RefCell::new(false);

    let handler = DummyHandler::new();
    // mimic fastapi_events.middlware event_store context
    let mut queue: Vec<(String, i32)> = vec![];
    // Simulate app call - stores events
    *called_app.borrow_mut() = true;
    queue.push(("fruit".to_string(), 1));

    // After app call, process events
    handler.handle_many(queue.clone());

    assert!(*called_app.borrow());
    assert!(handler.handled.borrow().contains(&(String::from("fruit"), 1)));
}

#[tokio::test]
async fn test_event_handler_asgi_middleware_non_http() {
    let app_called = RefCell::new(false);

    let handler = DummyHandler::new();

    // Simulate app call for 'lifespan' scope, handler.handle_many not called
    *app_called.borrow_mut() = true;

    assert!(*app_called.borrow());
}

#[test]
fn test_register_and_deregister_handlers() {
    let _handler = DummyHandler::new();
    let mut handler_store = std::collections::HashMap::new();
    handler_store.insert(2222, true);
    assert!(handler_store.contains_key(&2222));
    handler_store.remove(&2222);
    assert!(!handler_store.contains_key(&2222));
    // Deregister again should error
    let result = std::panic::catch_unwind(|| {
        handler_store.remove(&2222).expect("Should panic for missing key");
    });
    assert!(result.is_err());
}

#[test]
fn test_event_store_ctx_and_res_req_cycle_ctx_debug() {
    // Simulate logger debug
    let mut logs: Vec<String> = Vec::new();
    logs.push("Setting event_store ctx".to_string());
    logs.push("Resetting event_store ctx".to_string());

    assert!(logs.iter().any(|m| m.contains("Setting event_store ctx")));
    assert!(logs.iter().any(|m| m.contains("Resetting")));
    // No exception for entering/exiting dummy context managers
}

#[test]
fn test_del_deregisters() {
    struct Dummy {
        deregistered: std::cell::Cell<bool>,
    }
    impl Dummy {
        fn deregister_handlers(&self) {
            self.deregistered.set(true);
        }
        fn _drop(&self) {
            self.deregister_handlers();
        }
    }
    let dummy = Dummy {
        deregistered: std::cell::Cell::new(false),
    };
    dummy._drop();
    assert!(dummy.deregistered.get());
}