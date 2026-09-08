use paulocode_picostation::cmd::*;

#[test]
fn test_cmd_public() {
    reset_globals();

    // Public Test: interrupt_xlat CMD_AUTOSEQ, use 0xD and different values
    LATCHED.with(|l| *l.borrow_mut() = (3 << 20) | (0xD << 16));
    TRACK.with(|t| *t.borrow_mut() = 10);
    JUMP_TRACK.with(|jt| *jt.borrow_mut() = 4);
    interrupt_xlat(0, 0);
    TRACK.with(|t| assert_eq!(*t.borrow(), 10 - 4 * 2));
    SENS_DATA.with(|sd| {
        TRACK.with(|t| assert_eq!(sd.borrow()[2], if (*t.borrow() & 1) != 0 {1} else {0}));
    });

    // Public Test: interrupt_xlat CMD_SOCT sets soct and enables pio (again)
    reset_globals();
    LATCHED.with(|l| *l.borrow_mut() = (4 << 20));
    interrupt_xlat(0,0);
    SOCT.with(|s| assert_eq!(*s.borrow(), 1));

    // Public Test: CMD_JUMP_TRACK different value
    reset_globals();
    LATCHED.with(|l| *l.borrow_mut() = (5 << 20) | (0x2F3 << 4));
    interrupt_xlat(0,0);
    JUMP_TRACK.with(|jt| assert_eq!(*jt.borrow(), 0x2F3));

    // Public Test: sled_move FORWARD/REVERSE/STOP difference
    reset_globals();
    SLED_MOVE_DIRECTION.with(|dir| *dir.borrow_mut() = SLED_MOVE_STOP);
    LATCHED.with(|l| *l.borrow_mut() = (2 << 16));
    sled_move();
    SLED_MOVE_DIRECTION.with(|dir| assert_eq!(*dir.borrow(), SLED_MOVE_FORWARD));

    LATCHED.with(|l| *l.borrow_mut() = (3 << 16));
    sled_move();
    SLED_MOVE_DIRECTION.with(|dir| assert_eq!(*dir.borrow(), SLED_MOVE_REVERSE));

    LATCHED.with(|l| *l.borrow_mut() = (0 << 16));
    sled_move();
    SLED_MOVE_DIRECTION.with(|dir| assert_eq!(*dir.borrow(), SLED_MOVE_STOP));

    // Track increment/decrement when stopped (different start)
    LATCHED.with(|l| *l.borrow_mut() = (8 << 16));
    sled_move();
    TRACK.with(|t| assert_eq!(*t.borrow(), 1));

    LATCHED.with(|l| *l.borrow_mut() = (0xC << 16));
    sled_move();
    TRACK.with(|t| assert_eq!(*t.borrow(), 0));

    // Public Test: spindle sets SENS_data accordingly (different values)
    reset_globals();
    LATCHED.with(|l| *l.borrow_mut() = (6 << 16));
    spindle();
    SENS_DATA.with(|sd| assert_eq!(sd.borrow()[10], 1));

    LATCHED.with(|l| *l.borrow_mut() = (7 << 16));
    spindle();
    SENS_DATA.with(|sd| assert_eq!(sd.borrow()[10], 0));
}