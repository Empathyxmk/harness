// Rust translation of tests.c (core rope tests)

#[cfg(test)]
mod tests {
    use super::*;
    use crate::librope::*; // Adjust for actual Rust rope implementation

    #[test]
    fn test_basic_construction() {
        let rope = Rope::from_str("test");
        assert_eq!(rope.len(), 4);
        assert_eq!(rope.to_string(), "test");
    }

    #[test]
    fn test_append() {
        let mut rope = Rope::from_str("foo");
        rope.insert(3, "bar");
        assert_eq!(rope.to_string(), "foobar");
    }

    #[test]
    fn test_multibyte_utf8() {
        let mut rope = Rope::new();
        rope.insert(0, "😀😃😄😁");
        assert_eq!(rope.char_len(), 4);
        assert_eq!(rope.to_string(), "😀😃😄😁");
        rope.delete(0, 4);
        assert_eq!(rope.to_string(), "");
    }

    #[test]
    fn test_rope_utf8_boundaries() {
        let mut rope = Rope::from_str("main🐱cat");
        // Insert at ASCII boundary
        rope.insert(4, " ");
        assert_eq!(rope.to_string(), "main 🐱cat");
        // Deletion inside unicode boundary shouldn't panic, but let's try anyway:
        rope.delete(5, 1);
        assert_eq!(rope.to_string(), "main cat");
    }

    #[test]
    fn test_delete_entire_string() {
        let mut rope = Rope::from_str("erasure");
        rope.delete(0, rope.len());
        assert_eq!(rope.to_string(), "");
    }
}