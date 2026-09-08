use ysbaddaden_gc::array::Array;

#[test]
fn test_array_init() {
    let ary: Array<i32> = Array::new(64);
    assert_eq!(ary.size(), 0);
    assert!(ary.is_empty());
    assert_eq!(ary.buffer.capacity(), 64);
    assert_eq!(ary.buffer.as_ptr(), ary.buffer.as_ptr());
}

#[test]
fn test_array_lifetime() {
    let mut ary: Array<i32> = Array::new(2);

    let v = [1,2,3,4,5,6,7,8,9,10];
    for (i, x) in v.iter().enumerate() {
        ary.push(*x);
        assert_eq!(ary.size(), i+1);
    }
    // underlying buffer will grow, but check logic
    for i in (0..10).rev() {
        let w = ary.pop();
        assert_eq!(w, Some(v[i]));
    }
    assert_eq!(ary.pop(), None);
    assert_eq!(ary.size(), 0);
}