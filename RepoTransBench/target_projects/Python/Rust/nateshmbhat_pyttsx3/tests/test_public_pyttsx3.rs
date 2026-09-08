// Using dummy engine that reverses returns

use std::cell::RefCell;
use std::rc::Rc;
use std::collections::HashMap;

struct AnotherDummyEngine {
    driver_name: String,
}
impl AnotherDummyEngine {
    fn new(driver_name: &str) -> Self {
        Self { driver_name: driver_name.to_string() }
    }
    fn say(&self, text: &str) -> String {
        text.chars().rev().collect()
    }
    fn run_and_wait(&self) -> &'static str {
        "executed"
    }
    fn stop(&self) -> &'static str {
        "halted"
    }
}

thread_local! {
    static ENGINES: RefCell<HashMap<String, Rc<AnotherDummyEngine>>> = RefCell::new(HashMap::new());
}

fn init(driver_name: &str) -> Rc<AnotherDummyEngine> {
    ENGINES.with(|engines| {
        let mut engines = engines.borrow_mut();
        if let Some(e) = engines.get(driver_name) {
            return Rc::clone(e);
        }
        let instance = Rc::new(AnotherDummyEngine::new(driver_name));
        engines.insert(driver_name.to_string(), Rc::clone(&instance));
        instance
    })
}

#[test]
fn test_public_init_and_engine() {
    let engine = init("diffdummy");
    assert_eq!(engine.driver_name, "diffdummy");
}

#[test]
fn test_public_engine_cache() {
    let e1 = init("cachetestA");
    let e2 = init("cachetestA");
    assert!(Rc::ptr_eq(&e1, &e2));
}

#[test]
fn test_public_engine_unique() {
    let e1 = init("uniqueA");
    let e2 = init("uniqueB");
    assert!(!Rc::ptr_eq(&e1, &e2));
}

#[test]
fn test_public_engine_methods() {
    let e1 = init("diffdummy");
    assert_eq!(e1.say("bar"), "rab");
    assert_eq!(e1.run_and_wait(), "executed");
    assert_eq!(e1.stop(), "halted");
}