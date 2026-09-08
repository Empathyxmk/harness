#[cfg(test)]
mod tests {
    #[test]
    fn test_initialise_module() {
        colorama_initialise();
        assert!(initialised_correctly());
    }
}