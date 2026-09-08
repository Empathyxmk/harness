use haishoku_rs::haishoku::Haishoku;

#[test]
fn test_haishoku_main_color_distinct() {
    let hs = Haishoku::with_image_path("demo/demo_01.png");
    let main = hs.main_color;
    assert!(main.0 <= 255 && main.1 <= 255 && main.2 <= 255);
    assert!(main.0 != 199 || main.1 != 146 || main.2 != 117);
}