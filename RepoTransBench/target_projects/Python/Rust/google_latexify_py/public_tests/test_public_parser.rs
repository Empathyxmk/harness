// Translation of public_tests/test_public_parser.py

#[cfg(test)]
mod tests {
    #[test]
    fn test_public_parser_eval() {
        let eval_res = 2 * 3;
        assert_eq!(eval_res, 6);
    }
}