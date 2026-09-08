// Translated from tests/deye_events_test.py

#[cfg(test)]
mod tests {
    #[derive(Debug, PartialEq)]
    enum DeyeEvent {
        Started,
        Stopped,
        Error(String),
    }

    #[test]
    fn test_event_creation() {
        let evt1 = DeyeEvent::Started;
        let evt2 = DeyeEvent::Error("fail".to_string());
        assert_eq!(evt1, DeyeEvent::Started);
        match evt2 {
            DeyeEvent::Error(msg) => assert_eq!(msg, "fail"),
            _ => panic!("Expected error event"),
        };
    }
}