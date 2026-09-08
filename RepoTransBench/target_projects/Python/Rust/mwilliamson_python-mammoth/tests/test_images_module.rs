// Translated from tests/test_images_module.py

#[cfg(test)]
mod tests {
    use super::*;

    struct DummyImage {
        content_type: &'static str,
        data: &'static [u8],
        alt_text: Option<&'static str>,
    }

    impl DummyImage {
        fn new(content_type: &'static str, data: &'static [u8], alt_text: Option<&'static str>) -> Self {
            Self { content_type, data, alt_text }
        }

        fn open(&self) -> &[u8] {
            self.data
        }
    }

    #[test]
    fn test_img_element_adds_alt() {
        // let converter = images::img_element(|image| ...);
        // let img = DummyImage::new("foo/bar", b"bytes", Some("alt text here"));
        // ...
        panic!("Not yet implemented");
    }

    #[test]
    fn test_img_element_no_alt() {
        panic!("Not yet implemented");
    }

    #[test]
    fn test_data_uri_encodes_base64() {
        panic!("Not yet implemented");
    }

    #[test]
    fn test_inline_alias_works() {
        panic!("Not yet implemented");
    }
}