#[derive(Debug, PartialEq, Eq, Clone, Copy)]
struct Rect(i32, i32);

fn polygon_from_bbox(bbox: (i32, i32, i32, i32)) -> Vec<Rect> {
    let (x1, y1, x2, y2) = bbox;
    vec![
        Rect(x1, y1),
        Rect(x2, y1),
        Rect(x2, y2),
        Rect(x1, y2),
    ]
}

#[test]
fn test_polygon_from_bbox_public() {
    let bbox = (3, 4, 16, 22);
    let polygon = polygon_from_bbox(bbox);
    // Polygon goes clockwise
    assert_eq!(polygon, vec![Rect(3, 4), Rect(16, 4), Rect(16, 22), Rect(3, 22)]);
}

#[test]
fn test_polygon_from_bbox_zero_width_height_public() {
    let bbox = (10, 10, 10, 25);
    let polygon = polygon_from_bbox(bbox);
    assert_eq!(polygon, vec![Rect(10, 10), Rect(10, 10), Rect(10, 25), Rect(10, 25)]);
}