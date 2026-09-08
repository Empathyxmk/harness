use jwasham_practice_c_rust::interview::BitArray;

#[test]
fn test_bitsort_basic() {
    let n = 64;
    let mut bits = BitArray::new(n);

    for i in 0..n {
        bits.clr(i);
    }
    for i in (0..n).step_by(2) {
        bits.set(i);
    }
    for i in 0..n {
        if i % 2 == 0 { assert!(bits.test(i)); }
        else { assert!(!bits.test(i)); }
    }
    for i in 0..n {
        bits.clr(i);
    }
    for i in 0..n {
        assert!(!bits.test(i));
    }
}