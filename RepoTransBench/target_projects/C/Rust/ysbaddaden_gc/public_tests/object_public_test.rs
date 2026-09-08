use ysbaddaden_gc::object::Object;

#[test]
fn test_object_init_public() {
    let obj = Object::new(99, false, false);
    assert_eq!(obj.size, 99);
}