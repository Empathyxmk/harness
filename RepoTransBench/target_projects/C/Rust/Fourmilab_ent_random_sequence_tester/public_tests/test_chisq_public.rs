use fourmilab_ent_random_sequence_tester::chisq::pochisq;

#[test]
fn test_pochisq_public() {
    assert!(pochisq(0.5, 2) > 0.77);
    let v = pochisq(5.99, 2);
    assert!(v > 0.04 && v < 0.06);
    let val = pochisq(9.49, 4);
    assert!(val > 0.045 && val < 0.055);
    assert!(pochisq(-2.0, 3) > 0.99);
    assert!(pochisq(7.0, -2) > 0.99);
}