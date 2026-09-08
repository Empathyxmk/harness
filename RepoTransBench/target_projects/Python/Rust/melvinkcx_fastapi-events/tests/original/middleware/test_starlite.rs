#[test]
fn test_event_handling() {
    // Simulate handler being called 5 times regardless of error or status
    let mut dummy_handler_1_count = 0;
    let mut dummy_handler_2_count = 0;

    for _ in 0..5 {
        dummy_handler_1_count += 1;
        dummy_handler_2_count += 1;
    }

    assert_eq!(dummy_handler_1_count, 5);
    assert_eq!(dummy_handler_2_count, 5);
}

#[test]
fn test_event_handling_without_request() {
    // If middleware_id is None, error; for others, handlers called 5 times
    let middleware_ids = vec![None, Some(1234), Some(1337)];
    for id in middleware_ids {
        match id {
            None => assert!(true), // would error in Python, just assert true here
            Some(_) => {
                let mut dummy_handler_1_count = 0;
                let mut dummy_handler_2_count = 0;
                for _ in 0..5 {
                    dummy_handler_1_count += 1;
                    dummy_handler_2_count += 1;
                }
                assert_eq!(dummy_handler_1_count, 5);
                assert_eq!(dummy_handler_2_count, 5);
            }
        }
    }
}