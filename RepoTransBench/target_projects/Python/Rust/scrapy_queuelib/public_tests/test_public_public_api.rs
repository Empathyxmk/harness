#[test]
fn test_module_version_present_public() {
    use scrapy_queuelib::*;
    // Check presence of VERSION string
    assert!(VERSION.contains('.'));
}

#[test]
fn test_module_has_pqueue_and_rrqueue_public() {
    use scrapy_queuelib::*;
    // Here we check that the pqueue and rrqueue modules/classes exist
    // In Rust, tested by ability to import/use expected types
    use scrapy_queuelib::pqueue;
    use scrapy_queuelib::rrqueue;

    // Can instantiate these types:
    let _pq = pqueue::PriorityQueue::new();
    let _rrq = rrqueue::RoundRobinQueue::new();
}