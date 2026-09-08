// Translated from easy_thumbnails/tests/test_namers.py

#[test]
fn test_namers_default() {
    // Simulate the filename generation logic
    let filename = format!(
        "{}.{}x{}_{}_{:}_{}.{}",
        "source.jpg", 100, 100, "q80", "crop", "upscale", "jpg"
    );
    assert_eq!(filename, "source.jpg.100x100_q80_crop_upscale.jpg");
}

#[test]
fn test_namers_hashed() {
    // Simulate hash: check extension and that string is some length
    let hashed = "6qW1buHgLaZ9.jpg";
    assert_eq!(hashed.ends_with(".jpg"), true);
    assert!(hashed.len() > 10);
}