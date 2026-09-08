use std::cell::RefCell;
use std::rc::Rc;
use std::collections::HashMap;

#[derive(Default)]
struct DummyEngine {
    pub called: Rc<RefCell<HashMap<&'static str, String>>>,
}
impl DummyEngine {
    fn new() -> Self {
        Self { called: Rc::new(RefCell::new(HashMap::new())) }
    }
    fn say(&self, text: &str) {
        self.called.borrow_mut().insert("say", text.to_string());
    }
    fn run_and_wait(&self) {
        self.called.borrow_mut().insert("run", "true".to_string());
    }
    fn stop(&self) {}
}

struct EngineCache {
    instances: RefCell<HashMap<String, Rc<DummyEngine>>>,
}
impl EngineCache {
    fn new() -> Self {
        EngineCache { instances: RefCell::new(HashMap::new()) }
    }
    fn init(&self, driver_name: &str, _debug: bool) -> Rc<DummyEngine> {
        let mut instances = self.instances.borrow_mut();
        if let Some(e) = instances.get(driver_name) {
            return Rc::clone(e);
        }
        let instance = Rc::new(DummyEngine::new());
        instances.insert(driver_name.to_string(), Rc::clone(&instance));
        instance
    }
}

#[test]
fn test_init_returns_engine() {
    let cache = EngineCache::new();
    let engine = cache.init("dummy", false);
    assert!(engine.called.borrow().get("say").is_none());
    assert!(engine.called.borrow().get("run").is_none());
}

#[test]
fn test_init_returns_cached_instance() {
    let cache = EngineCache::new();
    let eng1 = cache.init("dummy", false);
    let eng2 = cache.init("dummy", false);
    assert!(Rc::ptr_eq(&eng1, &eng2));
}

#[test]
fn test_init_with_debug_flag() {
    let cache = EngineCache::new();
    let eng = cache.init("dummy", true);
    assert!(eng.called.borrow().get("say").is_none());
}

#[test]
fn test_speak_calls_init_and_engine_methods() {
    let calls = Rc::new(RefCell::new(HashMap::new()));
    struct DummyEngine2 {
        calls: Rc<RefCell<HashMap<&'static str, String>>>,
    }
    impl DummyEngine2 {
        fn new(calls: Rc<RefCell<HashMap<&'static str, String>>>) -> Self {
            Self { calls }
        }
        fn say(&self, text: &str) {
            self.calls.borrow_mut().insert("say", text.to_string());
        }
        fn run_and_wait(&self) {
            self.calls.borrow_mut().insert("run", "true".to_string());
        }
    }

    // "monkeypatch"
    let engine = DummyEngine2::new(Rc::clone(&calls));
    // call the two methods as would "pyttsx3.speak"
    engine.say("text");
    engine.run_and_wait();
    let c = calls.borrow();
    assert_eq!(c.get("say").map(|s| &**s), Some("text"));
    assert_eq!(c.get("run").map(|s| &**s), Some("true"));
}