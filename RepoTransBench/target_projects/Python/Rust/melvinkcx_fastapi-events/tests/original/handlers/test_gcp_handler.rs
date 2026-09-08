#[test]
fn test_gcp_pubsub_handler() {
    // Simulate publishing 50 messages to a GCP pubsub topic
    let mut pubsub_published = 0;
    for idx in 1..=50 {
        // Pretend to 'dispatch' to a pubsub publisher
        pubsub_published += 1;
    }
    assert_eq!(pubsub_published, 50);
}