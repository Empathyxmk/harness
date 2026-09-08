// Translated from tests.py

use asciimoo_drawille::{Canvas, line, Turtle};

#[test]
fn test_canvas_set() {
    let c = Canvas::new();
    c.set(0, 0);
    let chars = c.chars.borrow();
    assert!(chars.contains_key(&0) && chars[&0].contains_key(&0));
}

#[test]
fn test_canvas_unset_empty() {
    let c = Canvas::new();
    c.set(1, 1);
    c.unset(1, 1);
    let chars = c.chars.borrow();
    assert_eq!(chars.len(), 0);
}

#[test]
fn test_canvas_unset_nonempty() {
    let c = Canvas::new();
    c.set(0, 0);
    c.set(0, 1);
    c.unset(0, 1);
    let chars = c.chars.borrow();
    let value_any = chars[&0][&0].downcast_ref::<i32>().copied();
    assert_eq!(value_any, Some(1));
}

#[test]
fn test_canvas_clear() {
    let c = Canvas::new();
    c.set(1, 1);
    c.clear();
    let chars = c.chars.borrow();
    assert_eq!(chars.len(), 0);
}

#[test]
fn test_canvas_toggle() {
    let c = Canvas::new();
    c.toggle(0, 0);
    let chars = c.chars.borrow();
    assert_eq!(chars.len(), 1);
    assert_eq!(chars[&0].len(), 1);
    assert!(chars[&0][&0].downcast_ref::<i32>().is_some());
    c.toggle(0, 0);
    let chars2 = c.chars.borrow();
    assert_eq!(chars2.len(), 0);
}

#[test]
fn test_canvas_set_text() {
    let c = Canvas::new();
    c.set_text(0, 0, "asdf");
    assert_eq!(c.frame_no_args(), "asdf");
}

#[test]
fn test_canvas_frame() {
    let c = Canvas::new();
    assert_eq!(c.frame_no_args(), "");
    c.set(0, 0);
    assert_eq!(c.frame_no_args(), "⠁");
}

#[test]
fn test_canvas_max_min_limits() {
    let c = Canvas::new();
    c.set(0, 0);
    assert_eq!(c.frame(Some(2), None), "");
    assert_eq!(c.frame(None, Some(0)), "");
}

#[test]
fn test_canvas_get() {
    let c = Canvas::new();
    assert_eq!(c.get(0, 0), false);
    c.set(0, 0);
    assert_eq!(c.get(0, 0), true);
    assert_eq!(c.get(0, 1), false);
    assert_eq!(c.get(1, 0), false);
    assert_eq!(c.get(1, 1), false);
}

// Line tests

#[test]
fn test_line_single_pixel() {
    assert_eq!(line(0, 0, 0, 0), vec![(0, 0)]);
}

#[test]
fn test_line_row() {
    assert_eq!(line(0, 0, 1, 0), vec![(0, 0), (1, 0)]);
}

#[test]
fn test_line_column() {
    assert_eq!(line(0, 0, 0, 1), vec![(0, 0), (0, 1)]);
}

#[test]
fn test_line_diagonal() {
    assert_eq!(line(0, 0, 1, 1), vec![(0, 0), (1, 1)]);
}

// Turtle Tests

#[test]
fn test_turtle_position() {
    let mut t = Turtle::new();
    assert_eq!(t.pos_x, 0);
    assert_eq!(t.pos_y, 0);
    t.move_(1, 1);
    assert_eq!(t.pos_x, 1);
    assert_eq!(t.pos_y, 1);
}

#[test]
fn test_turtle_rotation() {
    let mut t = Turtle::new();
    assert_eq!(t.rotation, 0);
    t.right(30);
    assert_eq!(t.rotation, 30);
    t.left(30);
    assert_eq!(t.rotation, 0);
}

#[test]
fn test_turtle_brush() {
    let mut t = Turtle::new();
    assert_eq!(t.get(t.pos_x, t.pos_y), false);
    t.forward(1);
    assert_eq!(t.get(0, 0), true);
    assert_eq!(t.get(t.pos_x, t.pos_y), true);
    t.up();
    t.move_(2, 0);
    assert_eq!(t.get(t.pos_x, t.pos_y), false);
    t.down();
    t.move_(3, 0);
    assert_eq!(t.get(t.pos_x, t.pos_y), true);
}