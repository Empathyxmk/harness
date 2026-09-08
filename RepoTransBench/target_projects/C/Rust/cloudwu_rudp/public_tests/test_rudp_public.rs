use cloudwu_rudp::*;

// All public test cases below

#[test]
fn test_rudp_seq_incr_public() {
    let seq = 987654u32;
    let res = rudp_seq_incr(seq);
    assert_eq!(res, 987655u32);
}

#[test]
fn test_rudp_seq_diff_simple_public() {
    let a = 3000u32;
    let b = 1000u32;
    let diff = rudp_seq_diff(a, b);
    assert_eq!(diff, 2000);
}

#[test]
fn test_rudp_seq_diff_wrap_public() {
    let a = 10u32;
    let b = 4294967290u32;
    let diff = rudp_seq_diff(a, b);
    assert_eq!(diff, 16);
}

#[test]
fn test_rudp_seq_cmp_equal_public() {
    let a = 555555u32;
    let b = 555555u32;
    let cmp = rudp_seq_cmp(a, b);
    assert_eq!(cmp, 0);
}

#[test]
fn test_rudp_seq_cmp_ahead_public() {
    let a = 9001u32;
    let b = 123u32;
    let cmp = rudp_seq_cmp(a, b);
    assert_eq!(cmp, 1);
}

#[test]
fn test_rudp_seq_cmp_behind_public() {
    let a = 1234u32;
    let b = 5678u32;
    let cmp = rudp_seq_cmp(a, b);
    assert_eq!(cmp, -1);
}

#[test]
fn test_rudp_encode_decode_basic_public() {
    let mut buf = [0u8; 64];
    let mut p = RudpPacket::default();
    p.seq = 1000;
    p.ack = 10;
    p.flag = 2;
    p.len = 3;
    p.data[..4].copy_from_slice(b"abc\0");
    let len = rudp_encode_packet(&p, &mut buf);
    assert!(len > 0);

    let mut out = RudpPacket::default();
    let decode_len = rudp_decode_packet(&mut out, &buf[..len]);
    assert_eq!(decode_len, len);

    assert_eq!(out.seq, 1000);
    assert_eq!(out.ack, 10);
    assert_eq!(out.flag, 2);
    assert_eq!(out.len, 3);
    assert_eq!(
        std::str::from_utf8(&out.data[..out.len as usize]).unwrap(),
        "abc"
    );
}

#[test]
fn test_rudp_encode_decode_nontrivial_public() {
    let mut buf = [0u8; 128];
    let mut p = RudpPacket::default();
    p.seq = 5555;
    p.ack = 2121;
    p.flag = 3;
    let s = b"public-12345!!\0";
    p.data[..s.len()].copy_from_slice(s);
    p.len = s.len() as u32;

    let len = rudp_encode_packet(&p, &mut buf);
    assert!(len > 0);

    let mut out = RudpPacket::default();
    let decode_len = rudp_decode_packet(&mut out, &buf[..len]);
    assert_eq!(decode_len, len);

    assert_eq!(out.seq, 5555);
    assert_eq!(out.ack, 2121);
    assert_eq!(out.flag, 3);
    assert_eq!(out.len, s.len() as u32);
    assert_eq!(
        std::str::from_utf8(&out.data[..(out.len as usize - 1)]).unwrap(),
        "public-12345!!"
    );
}