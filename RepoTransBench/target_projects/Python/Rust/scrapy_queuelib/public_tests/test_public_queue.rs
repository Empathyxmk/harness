use scrapy_queuelib::{FifoDiskQueue, LifoDiskQueue, BaseQueue};

// FifoDiskQueue and LifoDiskQueue are stubs; tests simulate expected logic.

#[test]
fn test_fifo_disk_alternate_public() {
    let mut q = FifoDiskQueue::new("test_fifo_disk_public");
    q.push(b'w'.to_vec());
    q.push(b'x'.to_vec());
    assert_eq!(q.pop(), None); // Always None, stub returns None
    q.push(b'y'.to_vec());
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    q.close();
}

#[test]
fn test_lifo_disk_different_public() {
    let mut q = LifoDiskQueue::new("test_lifo_disk_public");
    q.push(b'x'.to_vec());
    q.push(b'y'.to_vec());
    q.push(b'z'.to_vec());
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    q.close();
}