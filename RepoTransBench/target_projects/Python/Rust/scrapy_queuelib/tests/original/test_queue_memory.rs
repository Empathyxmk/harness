use scrapy_queuelib::{FifoMemoryQueue, LifoMemoryQueue, BaseQueue};

struct DummyQueue;
impl BaseQueue<u8> for DummyQueue {
    fn push(&mut self, _obj: u8) {}
    fn pop(&mut self) -> Option<u8> { None }
    fn peek(&self) -> Option<u8> { None }
    fn close(&mut self) {}
    fn len(&self) -> usize { 0 }
}

#[test]
fn test_instance_and_subclass_check() {
    let mut _dummy = DummyQueue;
    assert_eq!(_dummy.len(), 0);
    assert_eq!(_dummy.peek(), None);
    assert_eq!(_dummy.pop(), None);
    // Rust doesn't have isinstance/issubclass the same way; trait is enough.
}

#[test]
fn test_fifo_memory_queue() {
    let mut q = FifoMemoryQueue::new();
    assert_eq!(q.len(), 0);
    q.push(1u8);
    q.push(2u8);
    assert_eq!(q.len(), 2);
    assert_eq!(q.peek(), Some(1u8));
    assert_eq!(q.pop(), Some(1u8));
    assert_eq!(q.peek(), Some(2u8));
    assert_eq!(q.pop(), Some(2u8));
    assert_eq!(q.peek(), None);
    assert_eq!(q.pop(), None);
}

#[test]
fn test_fifo_empty_pop_peek() {
    let mut q = FifoMemoryQueue::new();
    assert_eq!(q.pop(), None);
    assert_eq!(q.peek(), None);
}

#[test]
fn test_lifo_memory_queue() {
    let mut q = LifoMemoryQueue::new();
    assert_eq!(q.len(), 0);
    q.push('a');
    q.push('b');
    assert_eq!(q.len(), 2);
    assert_eq!(q.peek(), Some('b'));
    assert_eq!(q.pop(), Some('b'));
    assert_eq!(q.peek(), Some('a'));
    assert_eq!(q.pop(), Some('a'));
    assert_eq!(q.peek(), None);
    assert_eq!(q.pop(), None);
}