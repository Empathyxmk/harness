// Translated from tests_drawille_extra.py

use asciimoo_drawille::*;

#[test]
fn test_get_terminal_size_env() {
    // Simulate missing ioctl_GWINSZ and os.ctermid - env fallback
    let (width, height) = get_terminal_size_env(Some(("30", "100")));
    assert_eq!(width, 100);
    assert_eq!(height, 30);
}

#[test]
fn test_normalize_types() {
    // Supported types
    assert_eq!(normalize(&5i32), 5);
    assert_eq!(normalize(&4.7f64), 5);
    // Unsupported types
    let string_val = "a";
    let result = std::panic::catch_unwind(|| {
        normalize(&string_val)
    });
    assert!(result.is_err());
    let v: Vec<i32> = vec![1, 2];
    let result2 = std::panic::catch_unwind(|| {
        normalize(&v)
    });
    assert!(result2.is_err());
}

#[test]
fn test_intdefaultdict() {
    let mut d = intdefaultdict();
    assert_eq!(d["x"], 0);
}

#[test]
fn test_get_pos() {
    assert_eq!(get_pos(4.0, 8.0), (2, 2));
    assert_eq!(get_pos(1.4, 3.6), (0, 0));
}

#[test]
fn test_canvas_unset_unknown_type() {
    let c = Canvas::new();
    c.set(0, 0);
    // ".chars[0][0] = 'test'" in Python - Put a Box<str>
    {
        let mut chars = c.chars.borrow_mut();
        if let Some(row) = chars.get_mut(&0) {
            row.insert(0, Box::new("test".to_string()));
        }
    }
    c.unset(0, 0); // Should not panic
}

#[test]
fn test_canvas_set_invalid_type() {
    let c = Canvas::new();
    // ".chars[0][0] = 'str'" in Python - Put a Box<str>
    {
        let mut chars = c.chars.borrow_mut();
        if let Some(row) = chars.get_mut(&0) {
            row.insert(0, Box::new("str".to_string()));
        } else {
            let mut new_row = HashMap::new();
            new_row.insert(0, Box::new("str".to_string()));
            chars.insert(0, new_row);
        }
    }
    c.set(0, 0); // No exception
}

#[test]
fn test_canvas_toggle_cross_type() {
    let c = Canvas::new();
    {
        let mut chars = c.chars.borrow_mut();
        if let Some(row) = chars.get_mut(&0) {
            row.insert(0, Box::new("xx".to_string()));
        } else {
            let mut new_row = HashMap::new();
            new_row.insert(0, Box::new("xx".to_string()));
            chars.insert(0, new_row);
        }
    }
    c.toggle(0, 0); // Should not panic
}

#[test]
fn test_canvas_line_ending_property() {
    let c = Canvas::with_line_ending("END");
    assert_eq!(&c.line_ending, "END");
}