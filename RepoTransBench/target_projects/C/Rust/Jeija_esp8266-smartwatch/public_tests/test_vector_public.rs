use esp8266_smartwatch::vector::*;
use float_cmp::approx_eq;

#[test]
fn test_vector_basic_ops_public() {
    let a = Vector { x: -8.0, y: 5.0, z: 2.0 };
    let b = Vector { x: 1.0, y: 4.0, z: -7.0 };
    let c = vector_add(a, b);
    approx_eq!(f32, c.x, -7.0, ulps = 2);
    approx_eq!(f32, c.y, 9.0, ulps = 2);
    approx_eq!(f32, c.z, -5.0, ulps = 2);

    let c = vector_sub(a, b);
    approx_eq!(f32, c.x, -9.0, ulps = 2);
    approx_eq!(f32, c.y, 1.0, ulps = 2);
    approx_eq!(f32, c.z, 9.0, ulps = 2);

    let c = vector_scale(b, 3.0);
    approx_eq!(f32, c.x, 3.0, ulps = 2);
    approx_eq!(f32, c.y, 12.0, ulps = 2);
    approx_eq!(f32, c.z, -21.0, ulps = 2);

    let dot = vector_dot(a, b);
    approx_eq!(f32, dot, -8.0*1.0 + 5.0*4.0 + 2.0*-7.0, ulps = 2);

    let c = vector_cross(a, b);
    approx_eq!(f32, c.x, 5.0*-7.0-2.0*4.0, ulps = 2);
    approx_eq!(f32, c.y, 2.0*1.0-(-8.0)*-7.0, ulps = 2);
    approx_eq!(f32, c.z, -8.0*4.0-5.0*1.0, ulps = 2);

    let mag = vector_mag(b);
    approx_eq!(f32, mag, (1.0*1.0 + 4.0*4.0 + (-7.0)*(-7.0)).sqrt(), ulps = 2);
}