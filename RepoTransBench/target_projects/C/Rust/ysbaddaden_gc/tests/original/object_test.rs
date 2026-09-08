use ysbaddaden_gc::object::Object;

#[test]
fn test_object_init() {
    let obj = Object::new(55, false, false);
    assert_eq!(obj.size, 55);
    assert_eq!(obj.marked, false);
    assert_eq!(obj.atomic, false);
}