use std::fs::File;
use std::io::Write;
use bmp::*;

#[test]
fn test_public_bmp_functions() {
    // This is a placeholder for the public test
    // Will be updated after examining test_public.c
    
    // Basic size test
    assert_eq!(bmp_size(100, 100), 30054);
    
    // Create and initialize a small BMP
    let mut bmp = vec![0u8; BMP_SIZE!(10, 10)];
    bmp_init(&mut bmp, 10, 10);
    
    // Test width and height functions
    assert_eq!(bmp_width(&bmp), 10);
    assert_eq!(bmp_height(&bmp), 10);
    
    // Test color encoding/decoding
    let color = bmp_encode(0.5, 0.7, 0.9);
    let mut r = 0.0;
    let mut g = 0.0;
    let mut b = 0.0;
    bmp_decode(color, &mut r, &mut g, &mut b);
    
    assert!((r - 0.5).abs() < 0.01);
    assert!((g - 0.7).abs() < 0.01);
    assert!((b - 0.9).abs() < 0.01);
}