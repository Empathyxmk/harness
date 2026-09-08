use scrapy_queuelib::{FifoMemoryQueue, LifoMemoryQueue, BaseQueue};

struct AnotherDummyQueue;
impl BaseQueue<i32> for AnotherDummyQueue {
    fn push(&mut self, _obj: i32) {}
    fn pop(&mut self) -> Option<i32> { None }
    fn peek(&self) -> Option<i32> { None }
    fn close(&mut self) {}
    fn len(&self) -> usize { 0 }
}

#[test]
fn test_instance_and_subclass_public() {
    let mut _dummy = AnotherDummyQueue;
    assert_eq!(_dummy.len(), 0);
    assert_eq!(_dummy.peek(), None);
    assert_eq!(_dummy.pop(), None);
    // Traits provide interface in Rust
}

#[test]
fn test_fifo_memory_queue_public() {
    let mut q = FifoMemoryQueue::new();
    assert_eq!(q.len(), 0);
    q.push(100i32);
    q.push(200i32);
    q.push(300i32);
    assert_eq!(q.len(), 3);
    assert_eq!(q.peek(), Some(100));
    assert_eq!(q.pop(), Some(100));
    assert_eq!(q.peek(), Some(200));
    assert_eq!(q.pop(), Some(200));
    assert_eq!(q.peek(), Some(300));
    assert_eq!(q.pop(), Some(300));
    assert_eq!(q.peek(), None);
    assert_eq!(q.pop(), None);
}

#[test]
fn test_fifo_memory_queue_empty_public() {
    let mut q = FifoMemoryQueue::new();
    assert_eq!(q.peek(), None);
    assert_eq!(q.pop(), None);
}

#[test]
fn test_lifo_memory_queue_public() {
    let mut q = LifoMemoryQueue::new();
    assert_eq!(q.len(), 0);
    q.push('x');
    q.push('y');
    q.push('z');
    assert_eq!(q.len(), 3);
    assert_eq!(q.peek(), Some('z'));
    assert_eq!(q.pop(), Some('z'));
    assert_eq!(q.peek(), Some('y'));
    assert_eq!(q.pop(), Some('y'));
    assert_eq!(q.peek(), Some('x'));
    assert_eq!(q.pop(), Some('x'));
    assert_eq!(q.peek(), None);
    assert_eq!(q.pop(), None);
}