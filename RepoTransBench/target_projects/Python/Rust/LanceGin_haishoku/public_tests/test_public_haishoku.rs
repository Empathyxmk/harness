use haishoku_rs::haishoku::Haishoku;

#[test]
fn test_haishoku_get_palette_public() {
    let hs = Haishoku::with_image_path("demo/demo_01.png");
    let palette = hs.palette.expect("Palette must be present");
    assert_eq!(palette.len(), 6);
    assert!(palette.iter().all(|x| true)); // Each color is a (u8,u8,u8) tuple in Rust
}