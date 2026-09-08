// Translated from public_tests/test_public_drawille_extra.py

use asciimoo_drawille::*;

#[test]
fn test_get_terminal_size_env_public() {
    let (width, height) = get_terminal_size_env(Some(("33", "100")));
    assert_eq!(width, 100);
    assert_eq!(height, 33);
}

#[test]
fn test_normalize_types_public() {
    assert_eq!(normalize(&15i32), 15);
    assert_eq!(normalize(&17.8f64), 18);
    // Should error for empty Vec and string "xyz"
    let r1 = std::panic::catch_unwind(|| normalize(&Vec::<i32>::new()));
    assert!(r1.is_err());
    let s = "xyz";
    let r2 = std::panic::catch_unwind(|| normalize(&s));
    assert!(r2.is_err());
}

#[test]
fn test_intdefaultdict_public() {
    use std::ops::{Index, IndexMut};
    let mut d = intdefaultdict();
    assert_eq!(d["222"], 0);
    *d.get_mut("222") += 55;
    assert_eq!(d["222"], 55);
}

#[test]
fn test_get_pos_public() {
    assert_eq!(get_pos(7.0, 9.0), (3, 2));
    assert_eq!(get_pos(4.9, 15.2), (2, 3));
}

#[test]
fn test_canvas_unset_unknown_type_public() {
    let c = Canvas::new();
    c.set(4, 10);
    {
        let mut chars = c.chars.borrow_mut();
        if let Some(row) = chars.get_mut(&4) {
            row.insert(10, Box::new(vec![15i32, 30]));
        }
    }
    c.unset(4, 10); // Should not panic
}

#[test]
fn test_canvas_set_invalid_type_public() {
    let c = Canvas::new();
    {
        let mut chars = c.chars.borrow_mut();
        if let Some(row) = chars.get_mut(&6) {
            row.insert(7, Box::new(9.81f64));
        } else {
            let mut row = std::collections::HashMap::new();
            row.insert(7, Box::new(9.81f64));
            chars.insert(6, row);
        }
    }
    c.set(6, 7);
}

#[test]
fn test_canvas_toggle_cross_type_public() {
    let c = Canvas::new();
    {
        let mut chars = c.chars.borrow_mut();
        if let Some(row) = chars.get_mut(&9) {
            row.insert(12, Box::new(None::<i32>));
        } else {
            let mut row = std::collections::HashMap::new();
            row.insert(12, Box::new(None::<i32>));
            chars.insert(9, row);
        }
    }
    c.toggle(9, 12);
}

#[test]
fn test_canvas_line_ending_property_public() {
    let c = Canvas::with_line_ending("LF");
    assert_eq!(&c.line_ending, "LF");
}