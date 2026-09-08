use najoshi_sickle::{Kseq, Cutsites, fill_kseq, SANGER};
use najoshi_sickle::print_record::{print_record, print_record_N};
use std::io::Cursor;

#[test]
fn test_print_record() {
    let mut name = "foo";
    let mut comment = "my comment";
    let seq = "ACGTAAA";
    let qual = "IIIIIII";
    let mut kseq = Kseq::default();
    kseq.name.s = Some(name.to_string());
    kseq.name.l = name.len();
    kseq.comment.s = Some(comment.to_string());
    kseq.comment.l = comment.len();
    kseq.seq.s = Some(seq.to_string());
    kseq.seq.l = seq.len();
    kseq.qual.s = Some(qual.to_string());
    kseq.qual.l = qual.len();
    let cs = Cutsites { left: 0, right: 7, ..Default::default() };

    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &kseq, &cs).unwrap();

    let expected = "@foo my comment\nACGTAAA\n+\nIIIIIII\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);

    let mut buf2 = Cursor::new(Vec::new());
    print_record_N(&mut buf2, &kseq, SANGER).unwrap();
    let expected2 = "@foo my comment\nNNNNNNN\n+\nIIIIIII\n";
    assert_eq!(String::from_utf8(buf2.into_inner()).unwrap(), expected2);
}