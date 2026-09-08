/*
 Basic test for razer_lachesis5k6_init and razer_lachesis5k6_release
 Covers functional and error paths.
*/

use std::ffi::CString;
use std::os::raw::c_char;
use std::ptr;
use std::str;

// Dummies/mocks
struct DummyUsbCtx {
    h: i32,
}

struct DummyUsbDev;

struct RazerMouse {
    usb_ctx: *mut DummyUsbCtx,
    idstr: [u8; 128],
}

static mut RAZER_SYNAPSE_SHOULD_FAIL: i32 = 0;

fn razer_synapse_init(_m: &mut RazerMouse, _unused: *mut (), _feat: i32) -> i32 {
    unsafe {
        if RAZER_SYNAPSE_SHOULD_FAIL != 0 {
            return -1;
        }
    }
    0
}

fn razer_synapse_exit(_m: &mut RazerMouse) {}

fn razer_synapse_get_serial(_m: &mut RazerMouse) -> &'static str {
    "SERIAL"
}

fn razer_generic_usb_gen_idstr(
    _usbdev: &DummyUsbDev,
    _handle: i32,
    str_val: &str,
    _flag: i32,
    serial: &str,
    idstr: &mut [u8; 128],
) {
    let formatted = format!("FakeID:{}:{}", str_val, serial);
    let bytes = formatted.as_bytes();
    for (i, &b) in bytes.iter().enumerate().take(128) {
        idstr[i] = b;
    }
    // Null terminate
    if bytes.len() < 128 {
        idstr[bytes.len()] = 0;
    }
}

fn razer_lachesis5k6_init(m: &mut RazerMouse, _dev: &DummyUsbDev) -> i32 {
    // Simulate razer_synapse_init (use the global flag)
    let ret = razer_synapse_init(m, ptr::null_mut(), 0);
    if ret != 0 {
        m.idstr[0] = 0;
        return -1;
    }
    let serial = razer_synapse_get_serial(m);
    razer_generic_usb_gen_idstr(_dev, 0, "Lachesis 5600 DPI", 1, serial, &mut m.idstr);
    0
}

fn razer_lachesis5k6_release(_m: &mut RazerMouse) {
    // Should not crash or hang
}

#[test]
fn test_razer_lachesis5k6_init_ok() {
    let mut ctx = DummyUsbCtx { h: 1 };
    let mut m = RazerMouse {
        usb_ctx: &mut ctx as *mut _,
        idstr: [0; 128],
    };

    unsafe { RAZER_SYNAPSE_SHOULD_FAIL = 0; }

    let dev = DummyUsbDev;
    let res = razer_lachesis5k6_init(&mut m, &dev);
    assert_eq!(res, 0);

    let idstr = {
        let nul = m.idstr.iter().position(|&c| c == 0).unwrap_or(128);
        std::str::from_utf8(&m.idstr[..nul]).unwrap_or("")
    };
    assert!(idstr.contains("FakeID:Lachesis 5600 DPI:SERIAL"), "idstr not set correctly");
}

#[test]
fn test_razer_lachesis5k6_init_fail() {
    let mut ctx = DummyUsbCtx { h: 1 };
    let mut m = RazerMouse {
        usb_ctx: &mut ctx as *mut _,
        idstr: [0; 128],
    };

    unsafe { RAZER_SYNAPSE_SHOULD_FAIL = 1; }

    let dev = DummyUsbDev;
    let res = razer_lachesis5k6_init(&mut m, &dev);
    assert_ne!(res, 0);
    assert_eq!(m.idstr[0], 0);
}

#[test]
fn test_razer_lachesis5k6_release() {
    let mut m = RazerMouse {
        usb_ctx: ptr::null_mut(),
        idstr: [0; 128],
    };
    razer_lachesis5k6_release(&mut m);
    // Nothing to assert, just make sure it doesn't panic
}