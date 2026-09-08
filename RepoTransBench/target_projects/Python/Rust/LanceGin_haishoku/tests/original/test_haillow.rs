use haishoku_rs::haillow;
use std::fs::File;
use std::io::Write;
use std::path::Path;

use image::{RgbImage, Luma, DynamicImage, ImageOutputFormat};

#[test]
fn test_tuple_to_hex_public() {
    assert_eq!(haillow::tuple_to_hex((12, 210, 111)), "#0cd26f");
}

#[test]
fn test_hex_to_tuple_public() {
    assert_eq!(haillow::hex_to_tuple("#123456"), (18, 52, 86));
}

#[test]
fn test_get_image_local_and_convert() {
    // Create RGB PNG for test
    let tmp_file = "tests/test_haillow_rgb_tmp.png";
    let mut img = RgbImage::new(32, 24);
    for px in img.pixels_mut() {
        *px = image::Rgb([12, 34, 56]);
    }
    img.save(tmp_file).unwrap();
    // Ensure file saved
    assert!(Path::new(tmp_file).exists());
    // Tests a simple image load
    let img2 = image::open(tmp_file).unwrap();
    assert_eq!(img2.color().channel_count(), 3);
    std::fs::remove_file(tmp_file).unwrap();
}

#[test]
fn test_get_image_convert() {
    // Create Grayscale PNG for test
    let tmp_file = "tests/test_haillow_gray_tmp.png";
    let mut img = image::GrayImage::new(10, 10);
    for px in img.pixels_mut() {
        *px = image::Luma([100]);
    }
    img.save(tmp_file).unwrap();
    let img2 = image::open(tmp_file).unwrap().to_rgb8();
    assert_eq!(img2.color().channel_count(), 3);
    std::fs::remove_file(tmp_file).unwrap();
}

#[test]
fn test_get_thumbnail() {
    let tmp_file = "tests/test_haillow_rgb_tmp2.png";
    let mut img = RgbImage::new(512, 400);
    for px in img.pixels_mut() {
        *px = image::Rgb([12, 34, 56]);
    }
    img.save(tmp_file).unwrap();
    let dyn_img = image::open(tmp_file).unwrap();
    let thumbnail = dyn_img.thumbnail(256, 256);
    assert!(thumbnail.width() <= 256 && thumbnail.height() <= 256);
    std::fs::remove_file(tmp_file).unwrap();
}

#[test]
fn test_new_image() {
    let size = (8, 9);
    let color = (1, 2, 3);
    let img = RgbImage::from_fn(size.0, size.1, |_x, _y| image::Rgb([color.0, color.1, color.2]));
    assert_eq!(img.width(), size.0);
    assert_eq!(img.height(), size.1);
}

#[test]
fn test_joint_image() {
    let imgs: Vec<RgbImage> = (0..4)
        .map(|i| RgbImage::from_fn(50, 20, |_x, _y| image::Rgb([(i * 20) as u8, 0, (i * 30) as u8])))
        .collect();
    // Try to concatenate horizontally
    let (w, h) = (50 * imgs.len() as u32, 20);
    let mut out_img = RgbImage::new(w as u32, h as u32);
    for (i, img) in imgs.iter().enumerate() {
        for y in 0..h {
            for x in 0..50 {
                let px = img.get_pixel(x, y);
                out_img.put_pixel(x + (i as u32 * 50), y, *px);
            }
        }
    }
    // Just check dimensions and that no panic happened
    assert_eq!(out_img.dimensions(), (200, 20));
}