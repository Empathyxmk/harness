#[test]
fn test_aws_sqs_handler() {
    // Simulate 50 messages dispatched to a SQS-like queue
    let mut queue = Vec::new();
    for idx in 1..=50 {
        queue.push((String::from("new event"), format!("id:{}", idx)));
    }
    assert_eq!(queue.len(), 50);

    // Simulate receiving messages in batches of 10, five times
    for _ in 0..5 {
        let batch: Vec<_> = queue.drain(..10.min(queue.len())).collect();
        assert_eq!(batch.len(), 10);
    }
}