use ysbaddaden_gc::memory::{setzero, get_memory_limit};

#[test]
fn test_map_and_align() {
    let mut buf = [1u8; 16];
    setzero(&mut buf);
    for &b in buf.iter() {
        assert_eq!(b, 0);
    }
}
#[test]
fn test_get_memory_limit() {
    let l = get_memory_limit();
    assert!(l > 0);
}