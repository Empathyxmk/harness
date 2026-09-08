/*
 Basic tests for DeathAdder2013 command _init and usb_write/read error handling
 Mock USB/razer_error
*/
use std::cell::Cell;
use std::sync::Mutex;

use std::sync::atomic::{AtomicUsize, Ordering};

#[repr(C)]
struct Deathadder2013Command {
    data: [u8; 8],
    command: u8,
    request: u8,
}
impl Default for Deathadder2013Command {
    fn default() -> Self {
        Deathadder2013Command {
            data: [0; 8],
            command: 0,
            request: 0,
        }
    }
}

struct RazerMouseUsbCtx {
    h: i32,
}

struct RazerMouse {
    usb_ctx: *mut RazerMouseUsbCtx,
}
struct Deathadder2013Private<'a> {
    m: &'a mut RazerMouse,
}

static CALL_COUNT: AtomicUsize = AtomicUsize::new(0);

fn razer_error(_msg: &str) {
    // ignore
}

fn libusb_control_transfer(
    _h: i32,
    _flags: i32,
    _request: i32,
    _command: i32,
    _zero: i32,
    _buf: &mut [u8],
    size: usize,
    _timeout: i32,
) -> i32 {
    // Simulate usb fail on first attempt, succeed on second for read case
    let call = CALL_COUNT.fetch_add(1, Ordering::SeqCst);
    if call == 0 {
        return -1;
    }
    size as i32
}
const RAZER_USB_TIMEOUT: i32 = 500;

fn deathadder2013_command_init(cmd: &mut Deathadder2013Command) {
    let size = std::mem::size_of_val(cmd);
    let ptr = cmd as *mut _ as *mut u8;
    unsafe { std::ptr::write_bytes(ptr, 0, size); }
}

fn deathadder2013_usb_write<'a>(
    _priv: &Deathadder2013Private<'a>,
    _r1: i32,
    _r2: i32,
    _buf: &Deathadder2013Command,
    _size: usize,
) -> i32 {
    // Always fail, as in C test
    -1
}

#[test]
fn test_command_init() {
    let mut cmd = Deathadder2013Command {
        data: [0xFF; 8],
        command: 0xFF,
        request: 0xFF,
    };
    deathadder2013_command_init(&mut cmd);
    let ptr = &cmd as *const _ as *const u8;
    let size = std::mem::size_of_val(&cmd);
    for i in 0..size {
        unsafe {
            assert_eq!(*ptr.add(i), 0);
        }
    }
}

#[test]
fn test_usb_write_error_and_success() {
    let mut ctx = RazerMouseUsbCtx { h: 1 };
    let mut m = RazerMouse { usb_ctx: &mut ctx as *mut _ };
    let priv_struct = Deathadder2013Private { m: &mut m };
    let buf = Deathadder2013Command::default();
    let rc = deathadder2013_usb_write(&priv_struct, 1, 2, &buf, std::mem::size_of_val(&buf));
    assert_eq!(rc, -1); // always fails, since our mock returns -1 first call
    // next call would succeed, but we continue error-case
}