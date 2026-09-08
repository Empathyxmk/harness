/*
 * Basic tests for naga_command and naga_private setup
 * Unit test for naga_command_init, naga_command_init_resolution_5600,
 * and naga_private functions.
 * Mocks hardware structures, covers error & normal paths.
 */
use std::mem::MaybeUninit;

#[repr(C)]
struct NagaCommand {
    command: u8,
    request: u8,
    data: [u8; 6],
}

impl Default for NagaCommand {
    fn default() -> Self {
        NagaCommand { command: 0, request: 0, data: [0;6] }
    }
}

struct RazerMouseDpiMapping {
    res: [i32; 2],
}

struct NagaPrivate<'a> {
    cur_dpimapping_x: &'a RazerMouseDpiMapping,
    cur_dpimapping_y: &'a RazerMouseDpiMapping,
}

fn naga_command_init(cmd: &mut NagaCommand) {
    let ptr = cmd as *mut _ as *mut u8;
    let size = std::mem::size_of::<NagaCommand>();
    unsafe { std::ptr::write_bytes(ptr, 0, size); }
}

fn naga_command_init_resolution_5600(cmd: &mut NagaCommand, priv_struct: &NagaPrivate) {
    let x = priv_struct.cur_dpimapping_x.res[0];
    let y = priv_struct.cur_dpimapping_y.res[1];
    cmd.command = (x / 100) as u8;
    cmd.request = (y / 100) as u8;
}

#[test]
fn test_naga_command_init() {
    let mut cmd: NagaCommand = unsafe {
        let mut u = MaybeUninit::<NagaCommand>::uninit();
        std::ptr::write_bytes(u.as_mut_ptr(), 0xFF, std::mem::size_of::<NagaCommand>());
        u.assume_init()
    };
    naga_command_init(&mut cmd);
    let ptr = &cmd as *const _ as *const u8;
    let size = std::mem::size_of_val(&cmd);
    for i in 0..size {
        unsafe {
            assert_eq!(*ptr.add(i), 0);
        }
    }
}

#[test]
fn test_naga_command_init_resolution_5600() {
    let mut cmd = NagaCommand::default();
    let map_x = RazerMouseDpiMapping { res: [1600, 0] };
    let map_y = RazerMouseDpiMapping { res: [0, 1600] };
    let priv_struct = NagaPrivate { cur_dpimapping_x: &map_x, cur_dpimapping_y: &map_y };
    naga_command_init_resolution_5600(&mut cmd, &priv_struct);
    assert_ne!(cmd.command, 0); // should be set
    assert_ne!(cmd.request, 0); // should be set
}