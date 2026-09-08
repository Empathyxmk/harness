// Translation of src/latexify/transformers/prefix_trimmer_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_prefix_trimmer() {
        let s = "test_prefix";
        let trimmed = &s[5..];
        assert_eq!(trimmed, "_prefix");
    }
}