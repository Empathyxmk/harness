use najoshi_sickle::{Kseq, Cutsites, fill_kseq, SANGER};
use najoshi_sickle::print_record::print_record;
use std::io::Cursor;

#[test]
fn test_print_record_public() {
    let mut ks = Kseq::default();
    let mut cs = Cutsites::default();

    // Test: new name, no comment, longer sequence, new qualities
    fill_kseq(&mut ks, "Test123", None, "ATGCCGTA", "HHHHHHHH");
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    let expected = "@Test123\nATGCCGTA\n+\nHHHHHHHH\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);

    // Test: different sequence, single char, new qualities
    fill_kseq(&mut ks, "PubCase", Some("info"), "G", "Y");
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    let expected = "@PubCase info\nG\n+\nY\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);

    // Test: different sequence of 3, random letters, quality string
    fill_kseq(&mut ks, "RandName", None, "CTT", "III");
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    let expected = "@RandName\nCTT\n+\nIII\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);

    // Test: with comment, medium sequence
    fill_kseq(&mut ks, "EdgePub", Some("xyz"), "TGCA", "BBBB");
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    let expected = "@EdgePub xyz\nTGCA\n+\nBBBB\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);
}