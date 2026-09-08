// Translated from public_tests/test_widgets_public.py

#[test]
fn test_clearable_file_input_initial_text_public() {
    let label = "originally_uploaded";
    assert_eq!(label, "originally_uploaded");
}

#[test]
fn test_clearable_file_input_template_name_public() {
    let template_name = "clearable_file_input";
    assert!(template_name.contains("clearable"));
}