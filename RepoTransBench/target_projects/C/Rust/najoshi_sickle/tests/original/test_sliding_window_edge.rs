use najoshi_sickle::{Kseq, Cutsites, SANGER, fill_kseq};
use najoshi_sickle::sliding::sliding_window;

#[test]
fn test_sliding_window_edge() {
    // Fake a low-quality fastq record
    let mut kseq = Kseq::default();
    fill_kseq(&mut kseq, "edge", Some(""), "ACGTAAAA", "!!!!!!!!"); // '!' => Phred0
    let cuts = sliding_window(&kseq, SANGER, 2, 20, 0, 1, 1);
    assert_eq!(cuts.three_prime_cut, -1);
    assert_eq!(cuts.five_prime_cut, -1);
}