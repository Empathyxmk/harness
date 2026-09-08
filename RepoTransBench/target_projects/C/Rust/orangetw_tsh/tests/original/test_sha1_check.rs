use orangetw_tsh::sha1::*;

#[test]
fn test_sha1_simple() {
    let mut ctx = Sha1Context { data: vec![] };
    let mut digest = [0u8; 20];
    let msg = b"abc";
    sha1_starts(&mut ctx);
    sha1_update(&mut ctx, msg);
    sha1_finish(&ctx, &mut digest);

    let expected: [u8; 20] = [
        0xa9,0x99,0x3e,0x36,0x47,0x06,0x81,0x6a,0xba,0x3e,
        0x25,0x71,0x78,0x50,0xc2,0x6c,0x9c,0xd0,0xd8,0x9d
    ];
    assert_eq!(digest[..], expected[..], "SHA1 for 'abc' does not match");
}

#[test]
fn test_sha1_empty() {
    let mut ctx = Sha1Context { data: vec![] };
    let mut digest = [0u8; 20];
    sha1_starts(&mut ctx);
    sha1_update(&mut ctx, b"");
    sha1_finish(&ctx, &mut digest);

    let expected: [u8; 20] = [
        0xda,0x39,0xa3,0xee,0x5e,0x6b,0x4b,0x0d,0x32,0x55,
        0xbf,0xef,0x95,0x60,0x18,0x90,0xaf,0xd8,0x07,0x09
    ];
    assert_eq!(digest[..], expected[..], "SHA1 for empty string does not match");
}