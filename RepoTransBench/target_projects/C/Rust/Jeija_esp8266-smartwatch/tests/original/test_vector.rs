use esp8266_smartwatch::vector::*;
use float_cmp::approx_eq;

#[test]
fn test_vector_basic_ops() {
    let a = Vector { x: 1.0, y: 2.0, z: 3.0 };
    let b = Vector { x: 4.0, y: -5.0, z: 6.0 };
    let c = vector_add(a, b);
    approx_eq!(f32, c.x, 5.0, ulps = 2);
    approx_eq!(f32, c.y, -3.0, ulps = 2);
    approx_eq!(f32, c.z, 9.0, ulps = 2);

    let c = vector_sub(a, b);
    approx_eq!(f32, c.x, -3.0, ulps = 2);
    approx_eq!(f32, c.y, 7.0, ulps = 2);
    approx_eq!(f32, c.z, -3.0, ulps = 2);

    let c = vector_scale(a, 2.0);
    approx_eq!(f32, c.x, 2.0, ulps = 2);
    approx_eq!(f32, c.y, 4.0, ulps = 2);
    approx_eq!(f32, c.z, 6.0, ulps = 2);

    let dot = vector_dot(a, b);
    approx_eq!(f32, dot, 1.0*4.0 + 2.0*-5.0 + 3.0*6.0, ulps = 2);

    let c = vector_cross(a, b);
    approx_eq!(f32, c.x, 2.0*6.0-3.0*-5.0, ulps = 2);
    approx_eq!(f32, c.y, 3.0*4.0-1.0*6.0, ulps = 2);
    approx_eq!(f32, c.z, 1.0*-5.0-2.0*4.0, ulps = 2);

    let mag = vector_mag(a);
    approx_eq!(f32, mag, (1.0f32*1.0 + 2.0*2.0 + 3.0*3.0).sqrt(), ulps = 2);
}