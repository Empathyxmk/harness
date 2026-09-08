// Translation of: test/unit/test_mbuf.c

use std::fs::File;
use std::io::Write;

#[derive(Default)]
pub struct RteMempool {
    created: i32,
    name: [u8; 32],
}
#[derive(Default)]
pub struct RteMbuf {}
pub struct EthHdr { pub eth_type: u16 }
pub struct Iphdr { pub protocol: u8 }
pub struct Tcphdr {}
pub struct Ip6Hdr {}
pub struct WorkSpace { pub log: Option<File> }
pub struct MbufData { pub data: [u8;60] }

static mut G_CONFIG_JUMBO: i32 = 0;
static mut G_WORK_SPACE: Option<WorkSpace> = None;

fn mbuf_pool_create(_name: &str, _a: i32, _b: i32) -> Option<RteMempool> {
    // Always returns None (NULL) for test purposes
    None
}
fn mbuf_log(_mbuf: &RteMbuf, _desc: &str) {
    // Just a stub: would log packet info (simulated)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mbuf_pool_create() {
        let mp = mbuf_pool_create("mbuf", 0, 0);
        assert!(mp.is_none());
    }

    #[test]
    fn test_mbuf_log_runs() {
        let m = RteMbuf::default();
        let mut null_file = tempfile::NamedTempFile::new().unwrap();
        // set "global" workspace, simulate log to file
        unsafe {
            G_WORK_SPACE = Some(WorkSpace { log: Some(null_file.reopen().unwrap()) });
        }
        mbuf_log(&m, "test");
    }
}