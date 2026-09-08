#[cfg(test)]
mod tests {
    use std::fmt;

    #[derive(Debug)]
    struct FakeResponse {
        status_code: u16,
    }

    #[derive(Debug)]
    pub struct NuRequestException {
        response: FakeResponse,
    }

    #[test]
    fn test_exception_behavior() {
        let response = FakeResponse { status_code: 404 };
        let exception = NuRequestException { response };

        // Verify debug formatting for exception
        assert!(format!("{:?}", exception).contains("404"));
    }
}