use std::fs::File;
use std::io::Write;
use bmp::*;

#[test]
fn test_overflow() {
    // Overflow test
    assert_eq!(bmp_size(3, 178956966), 0x7ffffffe);
    assert_eq!(bmp_size(3, 178956967), 0);
    assert_eq!(bmp_size(0, 1), 0);
}

#[test]
fn test_bmp_creation() {
    const WIDTH: i64 = 1024;
    const HEIGHT: i64 = 1024;
    
    // Create buffer using the BMP_SIZE macro
    let mut bmp = vec![0u8; BMP_SIZE!(WIDTH, HEIGHT)];
    
    // Initialize the BMP
    bmp_init(&mut bmp, WIDTH, HEIGHT);
    
    // Fill the BMP with gradient colors
    for y in 0..HEIGHT {
        for x in 0..WIDTH {
            let r = y as f32 / HEIGHT as f32;
            let g = x as f32 / WIDTH as f32;
            let b = 1.0f32;
            bmp_set(&mut bmp, x, y, bmp_encode(r, g, b));
        }
    }
    
    // Verify the pixel colors
    for y in 0..HEIGHT {
        for x in 0..WIDTH {
            let r = y as f32 / HEIGHT as f32;
            let g = x as f32 / WIDTH as f32;
            let b = 1.0f32;
            
            let expected = bmp_encode(r, g, b);
            let actual = bmp_get(&bmp, x, y);
            
            let mut er = 0.0f32;
            let mut eg = 0.0f32;
            let mut eb = 0.0f32;
            
            let mut cr = 0.0f32;
            let mut cg = 0.0f32;
            let mut cb = 0.0f32;
            
            bmp_decode(actual, &mut cr, &mut cg, &mut cb);
            bmp_decode(expected, &mut er, &mut eg, &mut eb);
            
            assert_eq!(cr, er);
            assert_eq!(cg, eg);
            assert_eq!(cb, eb);
        }
    }
    
    // Write the BMP to a file
    let mut file = File::create("test.bmp").unwrap();
    file.write_all(&bmp).unwrap();
}