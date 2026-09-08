#[derive(Debug, Clone, Copy, PartialEq)]
struct Rect {
    left: f64,
    top: f64,
    width: f64,
    height: f64,
}

/// Calculate axis-aligned bounding box for a set of (x, y) points.
fn bounding_box<T: Copy + Into<(f64, f64)>>(pts: &[T]) -> Result<Rect, &'static str> {
    if pts.is_empty() {
        return Err("No points provided");
    }
    let mut min_x = std::f64::MAX;
    let mut min_y = std::f64::MAX;
    let mut max_x = std::f64::MIN;
    let mut max_y = std::f64::MIN;
    for &pt in pts {
        let (x, y) = pt.into();
        if x < min_x { min_x = x; }
        if y < min_y { min_y = y; }
        if x > max_x { max_x = x; }
        if y > max_y { max_y = y; }
    }
    Ok(Rect {
        left: min_x,
        top: min_y,
        width: max_x - min_x,
        height: max_y - min_y,
    })
}

/// Gift wrapping (Jarvis march) convex hull implementation for up to hundreds of points.
fn convex_hull(input: &[(f64, f64)]) -> Vec<(f64, f64)> {
    let mut points = input.to_vec();
    if points.len() < 3 {
        // Return input sorted lexicographically
        let mut sorted = points.clone();
        sorted.sort_by(|a, b| (a.0, a.1).partial_cmp(&(b.0, b.1)).unwrap());
        // But preserve order of Python test for two points
        if sorted.len() == 2 {
            return vec![sorted[0], sorted[1]];
        } else {
            return sorted;
        }
    }
    // Andrew's monotone chain
    points.sort_by(|a, b| (a.0, a.1).partial_cmp(&(b.0, b.1)).unwrap());
    let n = points.len();
    let mut lower = vec![];
    for &p in &points {
        while lower.len() >= 2 {
            let (q, r) = (lower[lower.len() - 2], lower[lower.len() - 1]);
            if cross(q, r, p) > 0.0 {
                lower.pop();
            } else {
                break;
            }
        }
        lower.push(p);
    }
    let mut upper = vec![];
    for &p in points.iter().rev() {
        while upper.len() >= 2 {
            let (q, r) = (upper[upper.len() - 2], upper[upper.len() - 1]);
            if cross(q, r, p) > 0.0 {
                upper.pop();
            } else {
                break;
            }
        }
        upper.push(p);
    }
    lower.pop();
    upper.pop();
    lower.extend(upper);
    lower
}

fn cross(o: (f64, f64), a: (f64, f64), b: (f64, f64)) -> f64 {
    (a.0 - o.0)*(b.1 - o.1) - (a.1 - o.1)*(b.0 - o.0)
}

#[test]
fn test_bounding_box() {
    // Should error on empty
    let empty = bounding_box::<(f64, f64)>(&[]);
    assert!(empty.is_err());

    // Degenerate case: single point
    let one = bounding_box(&[(0.0, 0.0)]);
    assert_eq!(one.unwrap(), Rect{left: 0.0, top: 0.0, width: 0.0, height: 0.0});

    // Four points forming box
    let pts = [(37.0, 551.0), (37.0, 625.0), (361.0, 626.0), (361.0, 550.0)];
    let box_res = bounding_box(&pts);
    assert_eq!(box_res.unwrap(), Rect{left: 37.0, top: 550.0, width: 324.0, height: 76.0});
}

#[test]
fn test_convex_hull_empty() {
    let result = convex_hull(&[]);
    assert_eq!(result, vec![]);
}

#[test]
fn test_convex_square() {
    let points = vec![(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)];
    let hull = convex_hull(&points);
    assert_eq!(hull, points);
}

#[test]
fn test_convex_duplicates() {
    let points = vec![(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)];
    let huge: Vec<_> = points.iter().cycle().take(points.len() * 10).cloned().collect();
    let hull = convex_hull(&huge);
    assert_eq!(hull, points);
}

#[test]
fn test_other() {
    let res = convex_hull(&[(1.0, 1.0), (2.0, 2.0), (3.0, 3.0), (1.0, 3.0)]);
    assert_eq!(res, vec![(1.0, 1.0), (1.0, 3.0), (3.0, 3.0)]);

    let res = convex_hull(&[
        (4.4, 14.0), (6.7, 15.25), (6.9, 12.8), (2.1, 11.1), (9.5, 14.9),
        (13.2, 11.9), (10.3, 12.3), (6.8, 9.5), (3.3, 7.7), (0.6, 5.1),
        (5.3, 2.4), (8.45, 4.7), (11.5, 9.6), (13.8, 7.3), (12.9, 3.1),
        (11.0, 1.1),
    ]);
    let expected = vec![
        (0.6, 5.1), (2.1, 11.1), (4.4, 14.0), (6.7, 15.25), (9.5, 14.9),
        (13.2, 11.9), (13.8, 7.3), (12.9, 3.1), (11.0, 1.1), (5.3, 2.4)
    ];
    assert_eq!(res, expected);
}