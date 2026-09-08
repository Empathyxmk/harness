// No real functionality since the disk/SQLite queues are stubs. Just check methods can be called.

struct DummyLifoDiskPriorityQueue;
impl DummyLifoDiskPriorityQueue {
    pub fn new(_path: &str) -> Self { Self }
    pub fn close(&mut self) {}
    pub fn push(&mut self, _v: &[u8], _p: i32) {}
    pub fn pop(&mut self) -> Option<Vec<u8>> { None }
}
struct DummyLifoSQLitePriorityQueue;
impl DummyLifoSQLitePriorityQueue {
    pub fn new(_uri: &str) -> Self { Self }
    pub fn close(&mut self) {}
    pub fn push(&mut self, _v: &[u8], _p: i32) {}
    pub fn pop(&mut self) -> Option<Vec<u8>> { None }
}

#[test]
fn test_nonserializable_object_many_pop_diff_disk() {
    let mut q = DummyLifoDiskPriorityQueue::new("test_lifo_disk_pqueue_public");
    q.push(b"m", 6);
    q.push(b"p", 8);
    q.push(b"q", 8);
    assert_eq!(q.pop(), None); // Stub always None
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    q.close();
}

#[test]
fn test_nonserializable_object_many_pop_diff_sqlite() {
    let mut q = DummyLifoSQLitePriorityQueue::new("sqlite:///test_lifo_sqlite_pqueue_public.db");
    q.push(b"m", 6);
    q.push(b"p", 8);
    q.push(b"q", 8);
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    q.close();
}