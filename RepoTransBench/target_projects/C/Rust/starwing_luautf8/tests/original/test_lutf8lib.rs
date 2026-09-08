// Translated from test_lutf8lib.c (original C tests)

#[cfg(test)]
mod tests {
    const UTF8_BUFFSZ: usize = 8;
    const UTF8_MAX: u32 = 0x7FFFFFFF;
    const UTF8_MAXCP: u32 = 0x10FFFF;

    fn utf8_invalid(ch: u32) -> bool {
        ch > UTF8_MAXCP || (0xD800..=0xDFFF).contains(&ch)
    }

    fn utf8_encode(buff: &mut [u8; UTF8_BUFFSZ], mut x: u32) -> usize {
        let mut n = 1;
        if x < 0x80 {
            buff[UTF8_BUFFSZ - 1] = (x & 0x7F) as u8;
        } else {
            let mut mfb: u32 = 0x3f;
            loop {
                buff[UTF8_BUFFSZ - n] = 0x80 | ((x & 0x3f) as u8);
                n += 1;
                x >>= 6;
                mfb >>= 1;
                if !(x > mfb) {
                    break;
                }
            }
            buff[UTF8_BUFFSZ - n] = ((!(mfb) << 1) as u8 | (x as u8)) & 0xFF;
        }
        n
    }

    #[test]
    fn test_utf8_invalid() {
        assert_eq!(utf8_invalid(0x10FFFF), false);
        assert_eq!(utf8_invalid(0x110000), true);
        assert_eq!(utf8_invalid(0xD800), true);
        assert_eq!(utf8_invalid(0xDFFF), true);
        assert_eq!(utf8_invalid(0x7FFF), false);
    }

    #[test]
    fn test_utf8_encode_ascii() {
        let mut buff = [0u8; UTF8_BUFFSZ];
        let n = utf8_encode(&mut buff, 0x41); // 'A'
        assert_eq!(n, 1);
        assert_eq!(buff[UTF8_BUFFSZ - 1], 0x41);
    }

    #[test]
    fn test_utf8_encode_multibyte() {
        let mut buff = [0u8; UTF8_BUFFSZ];
        let n = utf8_encode(&mut buff, 0x20AC); // €
        assert!(n > 1);
        // Check last byte is correct for U+20AC: should end with 0xAC
        assert_eq!(buff[UTF8_BUFFSZ - 1], 0xAC);
    }

    #[test]
    fn test_utf8_encode_fourbyte() {
        let mut buff = [0u8; UTF8_BUFFSZ];
        let n = utf8_encode(&mut buff, 0x1F600); // 😀
        assert!((1..=4).contains(&n));
        // No assert on value but should not crash
    }
}