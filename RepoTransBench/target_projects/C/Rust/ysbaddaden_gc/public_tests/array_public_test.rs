use ysbaddaden_gc::array::Array;

#[test]
fn test_array_init_push_access_public() {
    let mut array: Array<i32> = Array::new(6);
    let a = 10;
    let b = 99;
    let c = -5;
    let d = 201;
    let e = 33;
    let f = 101;
    assert_eq!(array.size(), 0);
    array.push(a);
    array.push(b);
    array.push(c);
    array.push(d);
    array.push(e);
    array.push(f);
    assert_eq!(array.size(), 6);
    assert_eq!(array.get(0), Some(&a));
    assert_eq!(array.get(1), Some(&b));
    assert_eq!(array.get(2), Some(&c));
    assert_eq!(array.get(3), Some(&d));
    assert_eq!(array.get(4), Some(&e));
    assert_eq!(array.get(5), Some(&f));
    array.clear();
    assert_eq!(array.size(), 0);
}