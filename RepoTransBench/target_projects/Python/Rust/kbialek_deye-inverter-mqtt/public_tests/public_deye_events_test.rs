// Public: Translated from public_tests/public_deye_events_test.py

#[derive(Debug, PartialEq)]
enum PublicDeyeEvent { Start, Fail(String) }

#[test]
fn test_event_public_create() {
    let ev = PublicDeyeEvent::Fail("oops".into());
    if let PublicDeyeEvent::Fail(msg) = ev {
        assert_eq!(msg, "oops");
    } else {
        panic!("Unexpected variant");
    }
}