use crate::event_handler::EventHandler;

#[test]
fn test_event_handler_modified() {
    let mut called = false;
    struct DummyHandler<'a> {
        called: &'a mut bool,
    }
    impl<'a> DummyHandler<'a> {
        fn on_modified(&mut self, _event: &str) {
            *self.called = true;
        }
    }
    let mut handler = DummyHandler { called: &mut called };
    handler.on_modified("afile.txt");
    assert!(called);
}