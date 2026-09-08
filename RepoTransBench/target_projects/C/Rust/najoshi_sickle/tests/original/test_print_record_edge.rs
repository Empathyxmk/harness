use najoshi_sickle::{fill_kseq, Kseq, Cutsites, SANGER};
use najoshi_sickle::print_record::{print_record, print_record_N};
use std::io::Cursor;

#[test]
fn test_print_record_edge() {
    let mut ks = Kseq::default();
    let mut cs = Cutsites::default();

    // Discarded record (left/right -1)
    fill_kseq(&mut ks, "A", Some(""), "ACGT", "IIII");
    cs.left = -1; cs.right = -1;
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    // No record printed (discarded)
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), "");

    // N handling
    fill_kseq(&mut ks, "B", Some(""), "NNNN", "IIII");
    let mut buf_n = Cursor::new(Vec::new());
    print_record_N(&mut buf_n, &ks, SANGER).unwrap();
    // Will print N's with qualities
    let expected = "@B\nNNNN\n+\nIIII\n";
    assert_eq!(String::from_utf8(buf_n.into_inner()).unwrap(), expected);

    // Partial trimming (cut in the middle)
    fill_kseq(&mut ks, "C", Some("foo"), "ACGTAC", "IIIIII");
    cs.left = 1; cs.right = 3;
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    // Comment must be present
    let expected = "@C foo\nCGT\n+\nIII\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);

    // Whole record
    fill_kseq(&mut ks, "D", Some(""), "GATTACA", "IIIIIII");
    cs.left = 0; cs.right = 6;
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    let expected = "@D\nGATTACA\n+\nIIIIIII\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);

    // Trimming edge/empty seq
    fill_kseq(&mut ks, "E", None, "", "");
    cs.left = 0; cs.right = -1;
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    let expected = "@E\n\n+\n\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);
}