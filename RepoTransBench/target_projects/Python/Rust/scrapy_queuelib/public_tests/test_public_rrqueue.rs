// No real functionality since disk/SQLite queues are stub-only.

struct DummyLifoDiskRRQueue;
impl DummyLifoDiskRRQueue {
    pub fn new(_path: &str) -> Self { Self }
    pub fn close(&mut self) {}
    pub fn push(&mut self, _v: &[u8], _p: i32) {}
    pub fn pop(&mut self) -> Option<Vec<u8>> { None }
}
struct DummyLifoSQLiteRRQueue;
impl DummyLifoSQLiteRRQueue {
    pub fn new(_uri: &str) -> Self { Self }
    pub fn close(&mut self) {}
    pub fn push(&mut self, _v: &[u8], _p: i32) {}
    pub fn pop(&mut self) -> Option<Vec<u8>> { None }
}

#[test]
fn test_nonserializable_object_many_pop_alt_disk() {
    let mut q = DummyLifoDiskRRQueue::new("test_lifo_disk_rrqueue_public");
    q.push(b"c", 4);
    q.push(b"e", 5);
    q.push(b"f", 5);
    assert_eq!(q.pop(), None); // Always None due to stub
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    q.close();
}

#[test]
fn test_nonserializable_object_many_pop_alt_sqlite() {
    let mut q = DummyLifoSQLiteRRQueue::new("sqlite:///test_lifo_sqlite_rrqueue_public.db");
    q.push(b"c", 4);
    q.push(b"e", 5);
    q.push(b"f", 5);
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    assert_eq!(q.pop(), None);
    q.close();
}