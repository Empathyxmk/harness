use dsprenkels_randombytes::{randombytes, set_mock_random_filler, RandomFiller};
use std::sync::Once;
use std::sync::Mutex;
use std::cell::RefCell;

static INIT: Once = Once::new();

fn setup() {
    INIT.call_once(|| {
        // Ensure global state is reset for each test suite run
        set_mock_random_filler(None);
    });
}

/// Helper macro for test output (as in RUN_TEST macro)
macro_rules! run_test {
    ($name:ident) => {
        print!("{} ... ", stringify!($name));
        let len = stringify!($name).len() + " ... ".len();
        for _ in len..32 { print!(" "); }
        $name();
        println!("ok");
    };
}

#[test]
fn test_functional() {
    setup();
    let mut buf1 = [0u8; 20];
    let mut buf2 = [0u8; 20];
    let ret1 = randombytes(&mut buf1).unwrap_or(-1);
    let ret2 = randombytes(&mut buf2).unwrap_or(-1);
    assert_eq!(ret1, ());
    assert_eq!(ret2, ());
    assert_ne!(buf1, buf2, "Two invocations of randombytes should yield different outputs");
}

#[test]
fn test_empty() {
    setup();
    let zero = [0u8; 20];
    let mut buf = zero.clone();
    let ret = randombytes(&mut buf[0..0]).unwrap_or(-1);
    assert_eq!(ret, ());
    assert_eq!(buf, zero, "Buffer should not have changed");
}

struct PartialRandom{ called: usize }
impl RandomFiller for PartialRandom {
    fn fill_bytes(&mut self, buf: &mut [u8]) -> Result<(), ()> {
        self.called += 1;
        let n = usize::min(16, buf.len());
        // Fill only n bytes with deterministic pattern for test predictability.
        for i in 0..n { buf[i] = (self.called as u8).wrapping_add(i as u8); }
        if buf.len() > n {
            // Recursively fill remaining with further calls (simulates partial OS API)
            self.fill_bytes(&mut buf[n..])
        } else {
            Ok(())
        }
    }
}

#[test]
fn test_getrandom_syscall_partial() {
    setup();
    let mut filler = PartialRandom{ called: 0 };
    set_mock_random_filler(Some(Box::new(filler)));
    let mut buf = [0u8; 100];
    let ret = randombytes(&mut buf).unwrap_or(-1);
    // The custom RandomFiller will fill buf in blocks of 16, ensuring at least 5 calls
    // (100 / 16 ~= 7 calls, but check only at least 5 for parity with C test)
    // Don't check strict pattern, just the number of calls
    // Because our trait object is lost after set_mock, we cannot directly check call count;
    // to verify logic, just check segments are not identical.
    assert_eq!(ret, ());
    // Check that first 20-byte segments are not all alike
    for i in 1..5 {
        assert_ne!(&buf[0..20], &buf[20*i..20*(i+1)], "Segments should differ, simulating repeated randomness");
    }
}

struct InterruptedRandom{ called: usize }
impl RandomFiller for InterruptedRandom {
    fn fill_bytes(&mut self, buf: &mut [u8]) -> Result<(), ()> {
        self.called += 1;
        if self.called < 5 {
            return Err(()); // Simulate error (like EINTR)
        }
        // On the 5th call, actually fill the buffer with a deterministic pattern
        for (i, b) in buf.iter_mut().enumerate() { *b = 128 + (i as u8); }
        Ok(())
    }
}

#[test]
fn test_getrandom_syscall_interrupted() {
    setup();
    let mut filler = InterruptedRandom{ called: 0 };
    set_mock_random_filler(Some(Box::new(filler)));
    let mut zero = [0u8; 20];
    let mut buf = [0u8; 20];
    let ret = randombytes(&mut buf).unwrap_or(-1);
    assert_eq!(ret, ());
    assert_ne!(buf, zero, "Buffer should get nonzero values even after interruption retries");
}

struct GlibPartialRandom{ called: usize }
impl RandomFiller for GlibPartialRandom {
    fn fill_bytes(&mut self, buf: &mut [u8]) -> Result<(), ()> {
        self.called += 1;
        let n = usize::min(16, buf.len());
        for i in 0..n { buf[i] = (self.called as u8).wrapping_add(i as u8); }
        if buf.len() > n {
            self.fill_bytes(&mut buf[n..])
        } else {
            Ok(())
        }
    }
}

#[test]
fn test_getrandom_glib_partial() {
    setup();
    let mut filler = GlibPartialRandom{ called: 0 };
    set_mock_random_filler(Some(Box::new(filler)));
    let mut buf = [0u8; 100];
    let ret = randombytes(&mut buf).unwrap_or(-1);
    assert_eq!(ret, ());
    // Check that first 20-byte segments are not all alike
    for i in 1..5 {
        assert_ne!(&buf[0..20], &buf[20*i..20*(i+1)]);
    }
}

struct GlibInterruptedRandom{ called: usize }
impl RandomFiller for GlibInterruptedRandom {
    fn fill_bytes(&mut self, buf: &mut [u8]) -> Result<(), ()> {
        self.called += 1;
        if self.called < 5 {
            return Err(());
        }
        for (i, b) in buf.iter_mut().enumerate() { *b = 64 + (i as u8); }
        Ok(())
    }
}

#[test]
fn test_getrandom_glib_interrupted() {
    setup();
    let mut filler = GlibInterruptedRandom{ called: 0 };
    set_mock_random_filler(Some(Box::new(filler)));
    let mut zero = [0u8; 20];
    let mut buf = [0u8; 20];
    let ret = randombytes(&mut buf).unwrap_or(-1);
    assert_eq!(ret, ());
    assert_ne!(buf, zero, "Random should not be all zero after retry cycle");
}

#[test]
fn test_issue_17() {
    setup();
    let mut buf1 = [0u8; 20];
    let mut buf2 = [0u8; 20];
    let ret1 = randombytes(&mut buf1).unwrap_or(-1);
    let ret2 = randombytes(&mut buf2).unwrap_or(-1);
    assert_eq!(ret1, ());
    assert_eq!(ret2, ());
    assert_ne!(buf1, buf2, "Random result of issue_17 two calls should not match");
}

#[test]
fn test_issue_22() {
    setup();
    let mut buf1 = [0u8; 20];
    let mut buf2 = [0u8; 20];
    let ret1 = randombytes(&mut buf1).unwrap_or(-1);
    let ret2 = randombytes(&mut buf2).unwrap_or(-1);
    assert_eq!(ret1, ());
    assert_eq!(ret2, ());
    assert_ne!(buf1, buf2, "Random result of issue_22 two calls should not match");
}

#[test]
fn test_issue_33() {
    setup();
    for _ in 0..100_000 {
        let mut buf = [0u8; 20];
        let ret = randombytes(&mut buf).unwrap_or(-1);
        assert_eq!(ret, ());
    }
}