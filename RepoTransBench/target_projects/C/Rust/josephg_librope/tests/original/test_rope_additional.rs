// Rust translation of test_rope_additional.c

#[cfg(test)]
mod tests {
    use super::*;
    use crate::librope::*; // adjust import to your Rust rope library

    #[test]
    fn test_insert_and_delete() {
        // Test inserting and deleting in a rope
        let mut rope = Rope::new();
        rope.insert(0, "hello");
        assert_eq!(rope.to_string(), "hello");

        rope.insert(5, " world");
        assert_eq!(rope.to_string(), "hello world");

        rope.delete(5, 6); // delete the space
        assert_eq!(rope.to_string(), "helloworld");

        rope.delete(0, 5); // delete "hello"
        assert_eq!(rope.to_string(), "world");
    }

    #[test]
    fn test_rope_split_and_concat() {
        let mut rope = Rope::from_str("abcdefghij");
        // Split into two ropes at position 5
        let second = rope.split_off(5);
        assert_eq!(rope.to_string(), "abcde");
        assert_eq!(second.to_string(), "fghij");

        // Concatenate back
        rope.concat(second);
        assert_eq!(rope.to_string(), "abcdefghij");
    }

    #[test]
    fn test_rope_insert_middle() {
        let mut rope = Rope::from_str("ace");
        rope.insert(1, "b");
        rope.insert(3, "d");
        rope.insert(5, "f");
        assert_eq!(rope.to_string(), "abcdef");
    }

    #[test]
    fn test_edge_cases() {
        let mut rope = Rope::new();
        rope.insert(0, "");
        assert_eq!(rope.to_string(), "");

        rope.insert(0, "a");
        assert_eq!(rope.to_string(), "a");

        rope.delete(0, 1);
        assert_eq!(rope.to_string(), "");

        // Delete on empty rope shouldn't panic
        rope.delete(0, 1);
        assert_eq!(rope.to_string(), "");
    }
}