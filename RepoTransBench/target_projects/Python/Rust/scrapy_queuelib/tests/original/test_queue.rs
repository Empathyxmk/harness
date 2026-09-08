#![allow(unused_imports)]
use scrapy_queuelib::*;
use tempfile::tempdir;

struct DummyQueue {
    q: Vec<Vec<u8>>,
}
impl DummyQueue {
    fn new() -> Self { DummyQueue { q: Vec::new() } }
}
impl BaseQueue<Vec<u8>> for DummyQueue {
    fn push(&mut self, obj: Vec<u8>) { self.q.push(obj) }
    fn pop(&mut self) -> Option<Vec<u8>> {
        if self.q.is_empty() { None } else { Some(self.q.pop().unwrap()) }
    }
    fn peek(&self) -> Option<Vec<u8>> {
        self.q.last().cloned()
    }
    fn close(&mut self) {}
    fn len(&self) -> usize { self.q.len() }
}

#[test]
fn test_interface_queue_triggers_not_implemented() {
    // For BaseQueue, Rust trait objects can't be new'd; we only test implementations.
    // If a method is not implemented the trait system will fail to compile.
}

#[test]
fn test_issubclass_like_rust() {
    // Rust trait system handles this at compile time. Here, just instantiating is "enough".
    let _d: DummyQueue = DummyQueue::new();
    let _ = FifoMemoryQueue::<Vec<u8>>::new();
    let _ = LifoMemoryQueue::<Vec<u8>>::new();
    let _ = FifoDiskQueue::new("tmp");
    let _ = LifoDiskQueue::new("tmp");
    let _ = FifoSQLiteQueue::new("tmp");
    let _ = LifoSQLiteQueue::new("tmp");
}

#[test]
fn test_isinstance_like_rust() {
    let mut _d: DummyQueue = DummyQueue::new();
    let mut f = FifoMemoryQueue::<Vec<u8>>::new();
    let mut l = LifoMemoryQueue::<Vec<u8>>::new();
    let mut fd = FifoDiskQueue::new("tmp");
    let mut ld = LifoDiskQueue::new("tmp");
    let mut fs = FifoSQLiteQueue::new("tmp");
    let mut ls = LifoSQLiteQueue::new("tmp");
    // All are their own type since Rust has static types.
}

trait QueueFactory {
    fn queue(&self) -> Box<dyn BaseQueue<Vec<u8>>>;
}

struct FifoMemQueueFactory;
impl QueueFactory for FifoMemQueueFactory {
    fn queue(&self) -> Box<dyn BaseQueue<Vec<u8>>> {
        Box::new(FifoMemoryQueue::<Vec<u8>>::new())
    }
}

#[test]
fn test_empty_queue() {
    let mut q = FifoMemoryQueue::<u8>::new();
    assert_eq!(q.pop(), None);
}

#[test]
fn test_single_pushpop() {
    let mut q = FifoMemoryQueue::<Vec<u8>>::new();
    q.push(vec![b'a']);
    assert_eq!(q.pop(), Some(vec![b'a']));
}

#[test]
fn test_binary_element() {
    let bytes = b"\x80\x02}".to_vec();
    let mut q = FifoMemoryQueue::<Vec<u8>>::new();
    q.push(bytes.clone());
    assert_eq!(q.pop(), Some(bytes));
}

#[test]
fn test_len_queue() {
    let mut q = FifoMemoryQueue::<u8>::new();
    assert_eq!(q.len(), 0);
    q.push(b'a');
    assert_eq!(q.len(), 1);
    q.push(b'b');
    q.push(b'c');
    assert_eq!(q.len(), 3);
    q.pop();
    q.pop();
    q.pop();
    assert_eq!(q.len(), 0);
}

#[test]
fn test_peek_one_element() {
    let mut q = FifoMemoryQueue::<u8>::new();
    assert_eq!(q.peek(), None);
    q.push(b'a');
    assert_eq!(q.peek(), Some(b'a'));
    assert_eq!(q.pop(), Some(b'a'));
    assert_eq!(q.peek(), None);
}

#[test]
fn test_fifo_push_pop() {
    let mut q = FifoMemoryQueue::<u8>::new();
    q.push(b'a');
    q.push(b'b');
    q.push(b'c');
    assert_eq!(q.pop(), Some(b'a'));
    assert_eq!(q.pop(), Some(b'b'));
    assert_eq!(q.pop(), Some(b'c'));
    assert_eq!(q.pop(), None);
}

#[test]
fn test_fifo_push_pop_interleaved() {
    let mut q = FifoMemoryQueue::<u8>::new();
    q.push(b'a');
    q.push(b'b');
    q.push(b'c');
    q.push(b'd');
    assert_eq!(q.pop(), Some(b'a'));
    assert_eq!(q.pop(), Some(b'b'));
    q.push(b'e');
    assert_eq!(q.pop(), Some(b'c'));
    assert_eq!(q.pop(), Some(b'd'));
    assert_eq!(q.pop(), Some(b'e'));
}

#[test]
fn test_fifo_peek_fifo() {
    let mut q = FifoMemoryQueue::<u8>::new();
    assert_eq!(q.peek(), None);
    q.push(b'a');
    q.push(b'b');
    q.push(b'c');
    assert_eq!(q.peek(), Some(b'a'));
    assert_eq!(q.peek(), Some(b'a'));
    assert_eq!(q.pop(), Some(b'a'));
    assert_eq!(q.peek(), Some(b'b'));
    assert_eq!(q.peek(), Some(b'b'));
    assert_eq!(q.pop(), Some(b'b'));
    assert_eq!(q.peek(), Some(b'c'));
    assert_eq!(q.peek(), Some(b'c'));
    assert_eq!(q.pop(), Some(b'c'));
    assert_eq!(q.peek(), None);
}

#[test]
fn test_lifo_push_pop() {
    let mut q = LifoMemoryQueue::<u8>::new();
    q.push(b'a');
    q.push(b'b');
    q.push(b'c');
    assert_eq!(q.pop(), Some(b'c'));
    assert_eq!(q.pop(), Some(b'b'));
    assert_eq!(q.pop(), Some(b'a'));
    assert_eq!(q.pop(), None);
}

#[test]
fn test_lifo_push_pop_interleaved() {
    let mut q = LifoMemoryQueue::<u8>::new();
    q.push(b'a');
    q.push(b'b');
    q.push(b'c');
    q.push(b'd');
    assert_eq!(q.pop(), Some(b'd'));
    assert_eq!(q.pop(), Some(b'c'));
    q.push(b'e');
    assert_eq!(q.pop(), Some(b'e'));
    assert_eq!(q.pop(), Some(b'b'));
    assert_eq!(q.pop(), Some(b'a'));
}

#[test]
fn test_lifo_peek_lifo() {
    let mut q = LifoMemoryQueue::<u8>::new();
    assert_eq!(q.peek(), None);
    q.push(b'a');
    q.push(b'b');
    q.push(b'c');
    assert_eq!(q.peek(), Some(b'c'));
    assert_eq!(q.peek(), Some(b'c'));
    assert_eq!(q.pop(), Some(b'c'));
    assert_eq!(q.peek(), Some(b'b'));
    assert_eq!(q.peek(), Some(b'b'));
    assert_eq!(q.pop(), Some(b'b'));
    assert_eq!(q.peek(), Some(b'a'));
    assert_eq!(q.peek(), Some(b'a'));
    assert_eq!(q.pop(), Some(b'a'));
    assert_eq!(q.peek(), None);
}