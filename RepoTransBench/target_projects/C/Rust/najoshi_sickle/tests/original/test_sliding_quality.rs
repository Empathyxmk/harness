use najoshi_sickle::{Kseq, fill_kseq, Cutsites, SANGER};
use najoshi_sickle::sliding::{get_quality_num, sliding_window};
use std::convert::TryInto;

#[test]
fn test_sliding_quality() {
    // All Phred+33, quality 40
    let mut kseq = Kseq::default();
    fill_kseq(&mut kseq, "test", Some(""), "ACGTAAA", "IIIIIII");

    // get_quality_num: valid
    let qval = get_quality_num('I', SANGER, &kseq, 2);
    assert_eq!(qval, ('I' as u8 - 33) as i32);

    // sliding_window: should return full-length cut
    let cuts = sliding_window(&kseq, SANGER, 2, 20, 0, 0, 0);
    assert!(cuts.five_prime_cut == 0 || cuts.five_prime_cut < 8);
    assert_eq!(cuts.three_prime_cut, 7);

    // Too short seq
    kseq.seq.l = 1;
    let cuts2 = sliding_window(&kseq, SANGER, 2, 20, 0, 0, 0);
    assert_eq!(cuts2.three_prime_cut, -1);
    assert_eq!(cuts2.five_prime_cut, -1);
}