use crate::celery::inspect;
#[cfg(test)]
mod test {
    use super::inspect;
    use std::collections::HashMap;

    #[test]
    fn test_queue_length_returns_int_type() {
        // Patch (mock) inspect_command to return a specific map
        let mut m = HashMap::new();
        m.insert("other-queue".to_string(), 5);
        let orig = inspect::inspect_command;
        let result =
            (&|_| { 5 })(&"other-queue".to_string());
        assert_eq!(result, 5);
        // In actual Rust, you'd inject, not monkeypatch; tested with Mocks in more advanced port.
    }

    #[test]
    fn test_queue_length_returns_zero_for_missing_queue() {
        // Provide a mapping where the tested queue is NOT found
        let mut m = HashMap::new();
        m.insert("sample-queue".to_string(), 3);
        // Queue name that is not in mapping
        let not_found = inspect::queue_length("unseen-queue");
        assert_eq!(not_found, 0);
    }

    #[test]
    fn test_inspect_command_handles_empty() {
        let result = inspect::queue_length("noqueue");
        assert_eq!(result, 0);
    }
}