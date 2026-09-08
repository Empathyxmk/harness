use fourmilab_ent_random_sequence_tester::randtest::{rt_init, rt_add, rt_end};

#[test]
fn test_entropy_basic_public() {
    let mut buf = [0u8; 16];
    for i in 0..16 {
        buf[i] = (15 - i) as u8;
    }
    rt_init(0);
    rt_add(&buf);
    let (r_ent, r_chisq, r_mean, r_montepicalc, r_scc) = rt_end();
    assert!(r_ent > 0.0);
    assert!(r_chisq >= 0.0);
    assert!((r_mean - 7.5).abs() <= 3.0);
    assert!(r_montepicalc > 0.0);
    assert!((-1.0..=1.0).contains(&r_scc));
}

#[test]
fn test_entropy_uniform_public() {
    let buf = [0x55u8; 64];
    rt_init(0);
    rt_add(&buf);
    let (_r_ent, _r_chisq, r_mean, _r_montepicalc, _r_scc) = rt_end();
    assert_eq!(r_mean, 0x55 as f64);
}