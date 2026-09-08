#[cfg(test)]
mod tests {
    #[test]
    fn test_use_colorama() {
        assert!(colorama_imports_work());
    }
}