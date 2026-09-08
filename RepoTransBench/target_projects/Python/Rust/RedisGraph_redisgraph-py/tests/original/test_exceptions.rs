#[cfg(test)]
mod tests {
    use super::super::super::src::exceptions::VersionMismatchException;
    #[test]
    fn test_version_mismatch_exception() {
        let ver = "2.10.0";
        let e = VersionMismatchException::new(ver);
        assert_eq!(e.version, ver);
    }
}