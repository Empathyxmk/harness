use dsprenkels_randombytes::{randombytes, set_mock_random_filler, RandomFiller};

/// Mock alternative getrandom for public test - simulate different test data
struct PatternFiller {
    pattern: [u8; 7],
    next_call: usize,
}
impl PatternFiller {
    fn new() -> Self {
        Self { pattern: [0xCC, 0x33, 0x99, 0x4B, 0xDE, 0x67, 0x18], next_call: 0 }
    }
}

impl RandomFiller for PatternFiller {
    fn fill_bytes(&mut self, buf: &mut [u8]) -> Result<(), ()> {
        for (i, x) in buf.iter_mut().enumerate() {
            *x = self.pattern[(i + self.next_call) % self.pattern.len()];
        }
        self.next_call += buf.len();
        Ok(())
    }
}

#[test]
fn public_randombytes_pattern_tests() {
    // Set up the deterministic pattern for mocking
    set_mock_random_filler(Some(Box::new(PatternFiller::new())));
    // 1. Generate 19 bytes and verify their content
    let mut buf = [0u8; 19];
    randombytes(&mut buf).expect("randombytes failed");
    let expected = [0xCC, 0x33, 0x99, 0x4B, 0xDE, 0x67, 0x18];
    for i in 0..19 {
        assert_eq!(buf[i], expected[i % 7], "Pattern mismatch at {}", i);
    }
    // 2. Fill buffer with different length (13)
    let mut buf2 = [0u8; 13];
    randombytes(&mut buf2).expect("randombytes failed");
    for j in 0..13 {
        assert_eq!(buf2[j], expected[j % 7], "Pattern mismatch in buf2 at {}", j);
    }
    // 3. Fill a buffer, change first byte, call again, confirm it is overwritten
    let mut buf3 = [0xFFu8; 10];
    randombytes(&mut buf3).expect("randombytes failed");
    assert_eq!(buf3[0], 0xCC);
    assert_eq!(buf3[3], 0x4B);
    assert_eq!(buf3[6], 0x18);
}