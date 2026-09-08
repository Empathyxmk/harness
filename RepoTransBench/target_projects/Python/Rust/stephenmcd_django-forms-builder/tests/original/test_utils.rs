use crate::forms_builder::forms::utils;

#[test]
fn test_is_file_extensions() {
    assert!(utils::is_file("photo.PNG"));
    assert!(utils::is_file("document.PDF"));
    assert!(!utils::is_file("example.txt"));
    assert!(!utils::is_file("no_dot"));
}

#[test]
fn test_slugify_basic() {
    let s = " Hello__World__ ";
    let sl = utils::slugify(s);
    assert_eq!(sl, "hello--world--");
}

#[test]
fn test_is_email_cases() {
    assert!(utils::is_email("foo@bar.com"));
    assert!(!utils::is_email("notanemail"));
    assert!(!utils::is_email("@nodomain"));
}

#[test]
fn test_content_as_txt_html() {
    struct Dummy;
    let text = utils::content_as_text(&Dummy);
    let html = utils::content_as_html(&Dummy);
    assert!(!text.is_empty());
    assert!(!html.is_empty());
}

#[test]
fn test_get_admin_url_format() {
    struct Dummy;
    impl utils::AdminMeta for Dummy {
        fn app_label(&self) -> &str { "myapp" }
        fn model_name(&self) -> &str { "dummy" }
        fn pk(&self) -> u32 { 1 }
    }
    let url = utils::get_admin_url(&Dummy);
    assert!(url.contains("myapp/dummy/1/"));
}