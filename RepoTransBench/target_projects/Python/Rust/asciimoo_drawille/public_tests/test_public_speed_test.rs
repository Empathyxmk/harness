// Translated from public_tests/test_public_speed_test.py

use asciimoo_drawille::Canvas;

#[test]
fn test_canvas_speed_public() {
    let c = Canvas::new();
    for y in (0..80).step_by(2) {
        c.set(15, y);
    }
    let buf = c.frame_no_args();

    // Buffer should not be empty and should contain braille chars
    assert!(buf.chars().any(|ch| ch as u32 >= 0x2800));
    c.clear();
    let buf2 = c.frame_no_args();
    assert!(!buf2.chars().any(|ch| ch as u32 >= 0x2800));
}