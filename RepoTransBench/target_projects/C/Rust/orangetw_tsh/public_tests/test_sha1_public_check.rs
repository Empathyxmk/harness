use orangetw_tsh::sha1::*;

#[test]
fn test_sha1_alphanumeric() {
    let mut ctx = Sha1Context { data: vec![] };
    let mut digest = [0u8; 20];
    // 'abc123'
    let msg = b"abc123";
    sha1_starts(&mut ctx);
    sha1_update(&mut ctx, msg);
    sha1_finish(&ctx, &mut digest);

    let expected: [u8; 20] = [
        0x63,0x36,0xe1,0x55,0xc4,0x71,0x41,0xa5,0x13,0x6e,
        0xe6,0x8a,0xe7,0x0d,0xb2,0x53,0x56,0x4e,0x29,0x4b
    ];
    assert_eq!(digest[..], expected[..], "SHA1 for 'abc123' incorrect");
}

#[test]
fn test_sha1_space() {
    let mut ctx = Sha1Context { data: vec![] };
    let mut digest = [0u8; 20];
    sha1_starts(&mut ctx);
    sha1_update(&mut ctx, b" ");
    sha1_finish(&ctx, &mut digest);

    let expected: [u8; 20] = [
        0xb8,0x84,0xfd,0x31,0x35,0xc0,0xea,0xb2,0x23,0xc5,
        0x18,0xdc,0xb5,0x29,0x26,0xec,0x76,0x23,0x6c,0xdc
    ];
    assert_eq!(digest[..], expected[..], "SHA1 for ' ' incorrect");
}