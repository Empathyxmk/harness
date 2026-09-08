use fourmilab_ent_random_sequence_tester::chisq::pochisq;

#[test]
fn test_pochisq() {
    assert!(pochisq(0.0, 1) > 0.99);
    let v = pochisq(3.84, 1);
    assert!(v > 0.04 && v < 0.06);
    assert!(pochisq(10.0, 5) < 0.1);
    assert!(pochisq(-1.0, 5) > 0.99);
    assert!(pochisq(5.0, 0) > 0.99);
}