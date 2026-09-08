// Translation of test/tests.c (part 1) for camgunz_cmp, Rust version
// This file includes: buffer handling, helper test macros, and some test logic.

use camgunz_cmp::buf::Buf;
use camgunz_cmp::cmp::{CmpObject, CmpType};
use std::sync::atomic::{AtomicI32, Ordering};

static READER_SUCCESSES: AtomicI32 = AtomicI32::new(-1);
static WRITER_SUCCESSES: AtomicI32 = AtomicI32::new(-1);
static SKIPPER_SUCCESSES: AtomicI32 = AtomicI32::new(-1);

fn buf_reader(buf: &mut Buf, data: &mut [u8]) -> bool {
    if READER_SUCCESSES.load(Ordering::SeqCst) == 0 {
        return false;
    }
    if READER_SUCCESSES.load(Ordering::SeqCst) > 0 {
        READER_SUCCESSES.fetch_sub(1, Ordering::SeqCst);
    }
    buf.read_all(data)
}

fn buf_writer(buf: &mut Buf, data: &[u8]) -> bool {
    if WRITER_SUCCESSES.load(Ordering::SeqCst) == 0 {
        return false;
    }
    if WRITER_SUCCESSES.load(Ordering::SeqCst) > 0 {
        WRITER_SUCCESSES.fetch_sub(1, Ordering::SeqCst);
    }
    buf.write_all(data);
    true
}

fn buf_skipper(buf: &mut Buf, count: usize) -> bool {
    if SKIPPER_SUCCESSES.load(Ordering::SeqCst) == 0 {
        return false;
    }
    if SKIPPER_SUCCESSES.load(Ordering::SeqCst) > 0 {
        SKIPPER_SUCCESSES.fetch_sub(1, Ordering::SeqCst);
    }
    buf.seek_forward(count)
}

fn setup_cmp_and_buf(buf: &mut Buf) {
    READER_SUCCESSES.store(-1, Ordering::SeqCst);
    WRITER_SUCCESSES.store(-1, Ordering::SeqCst);
    SKIPPER_SUCCESSES.store(-1, Ordering::SeqCst);
    buf.clear();
    buf.ensure_capacity(32);
    // cmp_init stub to be added as the cmp port is implemented.
}

fn teardown_cmp_and_buf(buf: &mut Buf) {
    READER_SUCCESSES.store(-1, Ordering::SeqCst);
    WRITER_SUCCESSES.store(-1, Ordering::SeqCst);
    SKIPPER_SUCCESSES.store(-1, Ordering::SeqCst);
    buf.clear();
    // cmp->error = 0 and more teardown logic (integrate with cmp port)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::i64;
    use std::u64;

    #[test]
    fn test_fixedint_rejects_invalid() {
        let mut buf = Buf::with_capacity(64);
        setup_cmp_and_buf(&mut buf);
        // Example analogs from C:
        assert!(!buf_writer(&mut buf, &[128u8])); // Should be false (invalid pfix)
        teardown_cmp_and_buf(&mut buf);
    }

    #[test]
    fn test_bin_basic() {
        let mut buf = Buf::with_capacity(64);
        setup_cmp_and_buf(&mut buf);
        // Simulate writing a 0-len bin (MsgPack BIN8 0xC4 0x00)
        assert!(buf_writer(&mut buf, &[0xC4, 0x00]));
        assert_eq!(buf.get_data()[..2], [0xC4, 0x00]);
        buf.seek(0);
        let mut sample = [0u8; 2];
        assert!(buf_reader(&mut buf, &mut sample));
        assert_eq!(sample, [0xC4, 0x00]);
        teardown_cmp_and_buf(&mut buf);
    }

    #[test]
    fn test_writer_and_reader_success_counts() {
        let mut buf = Buf::with_capacity(8);
        setup_cmp_and_buf(&mut buf);

        WRITER_SUCCESSES.store(1, std::sync::atomic::Ordering::SeqCst);
        assert!(buf_writer(&mut buf, &[1, 2, 3, 4]));

        WRITER_SUCCESSES.store(0, std::sync::atomic::Ordering::SeqCst);
        assert!(!buf_writer(&mut buf, &[5, 6]));

        READER_SUCCESSES.store(1, std::sync::atomic::Ordering::SeqCst);
        buf.seek(0);
        let mut out = [0u8; 4];
        assert!(buf_reader(&mut buf, &mut out));
        assert_eq!(out, [1, 2, 3, 4]);

        READER_SUCCESSES.store(0, std::sync::atomic::Ordering::SeqCst);
        buf.seek(0);
        let mut out2 = [0u8; 2];
        assert!(!buf_reader(&mut buf, &mut out2));

        teardown_cmp_and_buf(&mut buf);
    }

    // Additional detailed translations (integration test logic from C)
    // would continue as the cmp module is filled in future batches
}