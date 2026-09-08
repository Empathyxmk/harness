use std::cell::RefCell;
use std::rc::Rc;
use std::collections::HashMap;

// Dummy engine for rust test - mimics monkeypatching
#[derive(Default)]
struct DummyEngine {
    driver_name: String,
}
impl DummyEngine {
    fn new(driver_name: &str) -> Self {
        Self { driver_name: driver_name.into() }
    }
    fn say(&self, text: &str) -> String {
        text.to_owned()
    }
    fn run_and_wait(&self) -> &'static str {
        "ran"
    }
    fn stop(&self) -> &'static str {
        "stopped"
    }
}

// Emulate pyttsx3 engine cache for singleton behavior
thread_local! {
    static ENGINES: RefCell<HashMap<String, Rc<DummyEngine>>> = RefCell::new(HashMap::new());
}

fn init(driver_name: &str) -> Rc<DummyEngine> {
    ENGINES.with(|engines| {
        let mut engines = engines.borrow_mut();
        if let Some(e) = engines.get(driver_name) {
            return Rc::clone(e);
        }
        let instance = Rc::new(DummyEngine::new(driver_name));
        engines.insert(driver_name.to_string(), Rc::clone(&instance));
        instance
    })
}

#[test]
fn test_init_and_engine() {
    let engine = init("dummy");
    assert_eq!(engine.driver_name, "dummy");
}

#[test]
fn test_engine_cache() {
    let e1 = init("dummy");
    let e2 = init("dummy");
    assert!(Rc::ptr_eq(&e1, &e2));
}

#[test]
fn test_engine_unique() {
    let e1 = init("dummy1");
    let e2 = init("dummy2");
    assert!(!Rc::ptr_eq(&e1, &e2));
}

#[test]
fn test_engine_methods() {
    let e1 = init("dummy");
    assert_eq!(e1.say("foo"), "foo".to_string());
    assert_eq!(e1.run_and_wait(), "ran");
    assert_eq!(e1.stop(), "stopped");
}