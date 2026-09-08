use powergo_pytracking_rs::pytracking::{
    Configuration, TRACKING_PIXEL, PNG_MIME_TYPE, DEFAULT_TIMEOUT_SECONDS,
    get_click_tracking_url, get_click_tracking_result, get_open_tracking_result,
    get_open_tracking_url, get_open_tracking_url_path,
    get_click_tracking_url_path, get_open_tracking_pixel,
};

#[test]
fn test_init_exports_access() {
    let c = Configuration::default();
    assert_eq!(std::any::type_name::<Configuration>(), std::any::type_name::<Configuration>());
    assert!(TRACKING_PIXEL.len() > 0);
    assert_eq!(PNG_MIME_TYPE, "image/png");
    assert!(DEFAULT_TIMEOUT_SECONDS > 0);

    // Test callable exported functions by simply calling them
    let _ = get_click_tracking_url("", "", false);
    let _ = get_click_tracking_result("", "");
    let _ = get_open_tracking_result("", "");
    let _ = get_open_tracking_url("");
    let _ = get_open_tracking_url_path("", "");
    let _ = get_click_tracking_url_path("", "");
    let _ = get_open_tracking_pixel();
}