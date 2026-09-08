#[cfg(test)]
mod tests {
    #[test]
    fn test_public_initialise() {
        colorama_initialise();
        assert!(public_initialise_conditions_met());
    }
}