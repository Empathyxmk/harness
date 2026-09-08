use najoshi_sickle::{Kseq, Cutsites, fill_kseq};
use najoshi_sickle::print_record::print_record;
use std::io::Cursor;

#[test]
fn test_print_record_edge_public() {
    let mut ks = Kseq::default();
    let mut cs = Cutsites::default();

    // Empty description
    fill_kseq(&mut ks, "Alpha", None, "", "");
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    let expected = "@Alpha\n\n+\n\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);

    // Single letter sequence
    fill_kseq(&mut ks, "Beta", Some("note"), "N", "\u{4}");
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    let expected = "@Beta note\nN\n+\n\u{4}\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);

    // Short sequence, comment, quality
    fill_kseq(&mut ks, "Gamma", Some("bar"), "GT", "HH");
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    let expected = "@Gamma bar\nGT\n+\nHH\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);

    // No comment, 3-nt seq/qual
    fill_kseq(&mut ks, "Delta", None, "CCC", "FFF");
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    let expected = "@Delta\nCCC\n+\nFFF\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);

    // Empty seq/qual
    fill_kseq(&mut ks, "Epsilon", None, "", "");
    let mut buf = Cursor::new(Vec::new());
    print_record(&mut buf, &ks, &cs).unwrap();
    let expected = "@Epsilon\n\n+\n\n";
    assert_eq!(String::from_utf8(buf.into_inner()).unwrap(), expected);
}