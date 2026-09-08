use std::cell::RefCell;
use std::rc::Rc;
use std::collections::HashMap;
use pyttsx3_rust::dummy::{AnotherDummyEngine, AnotherDummyDriver};

struct TestDriverProxy {
    pub _driver: Rc<AnotherDummyDriver>,
    pub _engine: Rc<AnotherDummyEngine>,
    pub _busy: Rc<RefCell<bool>>,
    pub _queue: Rc<RefCell<Vec<(Box<dyn Fn() -> String>, Vec<String>, String)>>>,
    pub _name: String,
}
impl TestDriverProxy {
    fn make(driver_cls: fn() -> AnotherDummyDriver, name: &str) -> Self {
        let eng = Rc::new(AnotherDummyEngine::new());
        let driver = Rc::new(driver_cls());
        Self {
            _driver: driver,
            _engine: eng,
            _busy: Rc::new(RefCell::new(true)),
            _queue: Rc::new(RefCell::new(vec![])),
            _name: name.into(),
        }
    }
    pub fn set_busy(&self, val: bool) {
        *self._busy.borrow_mut() = val;
    }
    pub fn is_busy(&self) -> bool {
        *self._busy.borrow()
    }
    pub fn notify(&self, topic: &str, mut kw: HashMap<String, String>) {
        self._engine._notify(topic, kw);
    }
    pub fn push<F: 'static + Fn() -> String>(&self, func: F, args: Vec<String>, name: &str) {
        self._queue.borrow_mut().push((Box::new(func), args, name.to_string()));
    }
}

#[test]
fn test_public_driverproxy_init() {
    let proxy = TestDriverProxy::make(|| AnotherDummyDriver::new(), "otherdummy");
    assert!(proxy._busy.borrow().clone());
}

#[test]
fn test_public_driverproxy_del() {
    let _proxy = TestDriverProxy::make(|| AnotherDummyDriver::new(), "del");
    // Drop called automatically, no exception
}

#[test]
fn test_public_driverproxy_push_and_pump() {
    let proxy = TestDriverProxy::make(|| AnotherDummyDriver::new(), "push");
    // push uppercase function and reverse string function (simulates _push)
    let uppercase = || "fox".to_uppercase();
    let reverse = || "bottle".chars().rev().collect::<String>();
    proxy.push(uppercase, vec!["fox".into()], "");
    proxy.push(reverse, vec!["bottle".into()], "");
    // Drain the queue
    let mut collected = Vec::new();
    for (func, _, _) in proxy._queue.borrow_mut().drain(..) {
        collected.push(func());
    }
    assert_eq!(collected[0], "FOX");
    assert_eq!(collected[1], "elttob");
}

#[test]
fn test_public_driverproxy_notify() {
    let proxy = TestDriverProxy::make(|| AnotherDummyDriver::new(), "notify");
    let mut map = HashMap::new();
    map.insert("key".to_string(), "val".to_string());
    proxy.notify("pub_new_notify", map);
    let last = proxy._engine.notified.borrow().last().unwrap().clone();
    assert_eq!(last.0, "pub_new_notify");
    assert_eq!(last.1.get("key").map(|s| &**s), Some("val"));
}

#[test]
fn test_public_driverproxy_setbusy_and_isbusy() {
    let proxy = TestDriverProxy::make(|| AnotherDummyDriver::new(), "busy");
    proxy.set_busy(false);
    assert_eq!(proxy.is_busy(), false);
    proxy.set_busy(true);
    assert_eq!(proxy.is_busy(), true);
}

#[test]
fn test_public_driverproxy_say() {
    struct SayDriver {
        said_items: Rc<RefCell<Vec<(String, String)>>>
    }
    impl SayDriver {
        fn new() -> Self {
            SayDriver { said_items: Rc::new(RefCell::new(vec![])) }
        }
        fn say(&self, text: &str, name: &str) {
            self.said_items.borrow_mut().push((text.to_string(), name.to_string()));
        }
    }
    let say_driver = SayDriver::new();
    say_driver.say("Hi from public!", "pTestName");
    let items = say_driver.said_items.borrow();
    assert_eq!(items[0].0, "Hi from public!");
    assert_eq!(items[0].1, "pTestName");
}

#[test]
fn test_public_driverproxy_stop() {
    struct StopDriver {
        times_stopped: Rc<RefCell<u32>>,
    }
    impl StopDriver {
        fn new() -> Self {
            StopDriver { times_stopped: Rc::new(RefCell::new(0)) }
        }
        fn stop(&self) {
            *self.times_stopped.borrow_mut() += 1;
        }
    }
    let stop_driver = StopDriver::new();
    stop_driver.stop();
    assert_eq!(*stop_driver.times_stopped.borrow(), 1);
}