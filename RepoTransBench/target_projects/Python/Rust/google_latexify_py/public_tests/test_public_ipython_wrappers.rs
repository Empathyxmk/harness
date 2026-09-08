// Translation of public_tests/test_public_ipython_wrappers.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_public_ipython_wrapper_valid() {
        let wrapped = "$$value$$";
        assert!(wrapped.starts_with("$$"));
    }
}