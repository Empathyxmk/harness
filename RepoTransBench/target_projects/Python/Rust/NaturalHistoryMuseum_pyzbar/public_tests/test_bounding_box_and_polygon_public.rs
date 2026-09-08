#[derive(Debug, PartialEq, Eq, Clone, Copy)]
struct Rect(i32, i32);

fn bounding_box(pts: &[Rect]) -> (i32, i32, i32, i32) {
    let min_x = pts.iter().map(|r| r.0).min().unwrap();
    let min_y = pts.iter().map(|r| r.1).min().unwrap();
    let max_x = pts.iter().map(|r| r.0).max().unwrap();
    let max_y = pts.iter().map(|r| r.1).max().unwrap();
    (min_x, min_y, max_x, max_y)
}

#[test]
fn test_bounding_box_rect_public() {
    let pts = [Rect(5, 7), Rect(25, 7), Rect(25, 32), Rect(5, 32)];
    let box1 = bounding_box(&pts);
    assert_eq!(box1, (5, 7, 25, 32));
    // Mix order for robustness
    let pts_reorder = [Rect(25, 32), Rect(25, 7), Rect(5, 32), Rect(5, 7)];
    let box2 = bounding_box(&pts_reorder);
    assert_eq!(box2, (5, 7, 25, 32));
}

#[test]
fn test_bounding_box_negative_coords_public() {
    let pts = [Rect(-12, -8), Rect(0, -8), Rect(0, 2), Rect(-12, 2)];
    assert_eq!(bounding_box(&pts), (-12, -8, 0, 2));
}