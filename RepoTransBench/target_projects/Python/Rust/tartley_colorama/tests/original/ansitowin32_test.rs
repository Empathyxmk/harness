#[cfg(test)]
mod tests {
    #[test]
    fn test_write_and_convert() {
        let converter = AnsiToWin32::new(std::io::stdout());
        converter.write("\x1b[31mRed text\x1b[0m");
        assert!(written_correctly());
    }
}