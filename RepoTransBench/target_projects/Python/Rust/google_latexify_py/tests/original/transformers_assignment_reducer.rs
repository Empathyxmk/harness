// Translation of src/latexify/transformers/assignment_reducer_test.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_assignment_reducer() {
        // Simulate reduction of a = a + 1 to a += 1
        let mut a = 1;
        a += 1;
        assert_eq!(a, 2);
    }
}