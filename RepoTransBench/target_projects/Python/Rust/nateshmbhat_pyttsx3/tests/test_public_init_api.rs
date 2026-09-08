use std::cell::RefCell;
use std::rc::Rc;
use std::collections::HashMap;

struct YetAnotherDummyEngine {
    name: String,
}
impl YetAnotherDummyEngine {
    fn new(driver_name: &str) -> Self {
        Self { name: driver_name.to_string() }
    }
    fn start(&self) -> &'static str { "hello" }
    fn finish(&self) -> &'static str { "goodbye" }
}

thread_local! {
    static ENGINES: RefCell<HashMap<String, Rc<YetAnotherDummyEngine>>> = RefCell::new(HashMap::new());
}

fn init(driver_name: &str) -> Rc<YetAnotherDummyEngine> {
    ENGINES.with(|engines| {
        let mut engines = engines.borrow_mut();
        if let Some(e) = engines.get(driver_name) {
            return Rc::clone(e);
        }
        let instance = Rc::new(YetAnotherDummyEngine::new(driver_name));
        engines.insert(driver_name.to_string(), Rc::clone(&instance));
        instance
    })
}

#[test]
fn test_public_engine_creation() {
    let e = init("publicengine");
    assert_eq!(&e.name, "publicengine");
}

#[test]
fn test_public_engine_singleton() {
    let e1 = init("publicdummyA");
    let e2 = init("publicdummyA");
    assert!(Rc::ptr_eq(&e1, &e2));
}

#[test]
fn test_public_engine_different() {
    let e1 = init("public1");
    let e2 = init("public2");
    assert!(!Rc::ptr_eq(&e1, &e2));
}