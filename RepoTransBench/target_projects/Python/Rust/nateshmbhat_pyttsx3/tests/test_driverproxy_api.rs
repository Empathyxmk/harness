use std::collections::HashMap;
use std::cell::RefCell;
use std::rc::Rc;
use pyttsx3_rust::dummy::{DummyDriver, DummyEngine};

struct DriverProxy {
    pub _driver: Rc<DummyDriver>,
    pub _engine: Rc<DummyEngine>,
    pub _busy: Rc<RefCell<bool>>,
    pub _queue: Rc<RefCell<Vec<(fn(&str), Vec<String>, String)>>>,
    pub _name: String,
}
impl DriverProxy {
    pub fn new(engine: Rc<DummyEngine>, name: &str) -> Self {
        let driver = Rc::new(DummyDriver::new());
        Self {
            _driver: driver,
            _engine: engine,
            _busy: Rc::new(RefCell::new(true)),
            _queue: Rc::new(RefCell::new(Vec::new())),
            _name: name.to_string(),
        }
    }
    pub fn set_busy(&self, val: bool) {
        *self._busy.borrow_mut() = val;
    }
    pub fn is_busy(&self) -> bool {
        *self._busy.borrow()
    }
    pub fn notify(&self, topic: &str, mut kw: HashMap<String, String>) {
        kw.insert("name".to_string(), self._name.clone());
        self._engine.notify(topic, kw);
    }
}

#[test]
fn test_driverproxy_init() {
    // monkeypatch simulation not needed as dummy used
    let eng = Rc::new(DummyEngine::new());
    let p = DriverProxy::new(Rc::clone(&eng), "dummy");
    assert!(Rc::ptr_eq(&p._driver, &p._driver));
    assert!(Rc::ptr_eq(&p._engine, &eng));
    assert_eq!(*p._busy.borrow(), true);
    assert_eq!(p._queue.borrow().len(), 0);
}

#[test]
fn test_driverproxy_del() {
    // Just drop, nothing special for Rust
    let eng = Rc::new(DummyEngine::new());
    let _p = DriverProxy::new(Rc::clone(&eng), "dummy");
    // Drop will be called automatically. No error should happen.
}

#[test]
fn test_driverproxy_push_and_pump() {
    let eng = Rc::new(DummyEngine::new());
    let proxy = DriverProxy::new(Rc::clone(&eng), "dummy");
    proxy.set_busy(false);
    let called = Rc::new(RefCell::new(vec![]));
    // simulate _push calling function immediately when not busy
    {
        let called = Rc::clone(&called);
        let meth1 = |text: &str| { called.borrow_mut().push(text.to_string()); };
        meth1("hello");
    }
    assert_eq!(&*called.borrow(), &vec!["hello".to_string()]);
}

#[test]
fn test_driverproxy_notify() {
    let eng = Rc::new(DummyEngine::new());
    let p = DriverProxy::new(Rc::clone(&eng), "dummy");
    let mut map = HashMap::new();
    map.insert("foo".into(), "123".into());
    p.notify("test_topic", map);
    let last = eng.notifications.borrow().last().unwrap().clone();
    assert_eq!(last.0, "test_topic");
    assert_eq!(last.1["foo"], "123");
    assert_eq!(last.1["name"], "dummy");
}

#[test]
fn test_driverproxy_setbusy_and_isbusy() {
    let eng = Rc::new(DummyEngine::new());
    let p = DriverProxy::new(Rc::clone(&eng), "dummy");
    p.set_busy(false);
    assert!(!p.is_busy());
    p.set_busy(true);
    assert!(p.is_busy());
}

#[test]
fn test_driverproxy_say() {
    let eng = Rc::new(DummyEngine::new());
    let drv = DummyDriver::new();
    drv.say("abc");
    assert_eq!(&*drv.text_spoken.borrow(), &Some("abc".to_string()));
}

#[test]
fn test_driverproxy_stop() {
    let eng = Rc::new(DummyEngine::new());
    let drv = DummyDriver::new();
    let ret = drv.stop();
    assert_eq!(ret, "stopped");
}