#[cfg(test)]
mod tests {
    #[derive(Debug)]
    struct Image { data: Vec<u8> }
    #[test]
    fn test_get_image() {
        let image = Image { data: vec![137, 80, 78, 71 /*... signature bytes for PNG or JPEG ...*/]};
        assert!(!image.data.is_empty());
    }
}