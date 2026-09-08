use ysbaddaden_gc::memory::setzero;

#[test]
fn test_memory_setzero_public() {
    let mut buf = [1u8,2,3,4,5,6,7];
    setzero(&mut buf);
    for b in buf.iter() {
        assert_eq!(*b, 0);
    }
}