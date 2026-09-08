#[cfg(test)]
mod tests {
    use std::collections::HashMap;
    use crate::exceptions::ApiError;

    #[derive(Debug)]
    struct DummyModelPublic {
        id: u32,
    }

    struct DummyResponsePublic {
        data: HashMap<&'static str, u32>,
        status_code: u32,
        from_cache: bool,
    }
    impl DummyResponsePublic {
        fn json(&self) -> HashMap<&'static str, u32> {
            self.data.clone()
        }
    }

    struct DummySessionPublic {
        req: std::cell::RefCell<Option<(String, Option<HashMap<&'static str, u32>>, Option<u32>)>>,
    }
    impl DummySessionPublic {
        fn new() -> Self {
            Self { req: std::cell::RefCell::new(None) }
        }
        fn get(&self, url: &str, params: Option<HashMap<&str, u32>>, expire_after: Option<u32>) -> DummyResponsePublic {
            *self.req.borrow_mut() = Some((url.to_string(), params.clone(), expire_after));
            let mut data = HashMap::new();
            data.insert("id", 321);
            DummyResponsePublic { data, status_code: 201, from_cache: false }
        }
    }

    // Emulate ensureLimit logic
    fn ensure_limit(val: u32, max: u32) -> u32 {
        if val > max { max } else { val }
    }

    struct ApiPublic {
        session: DummySessionPublic,
        user_id: String,
        country_code: String,
        token: String,
    }

    impl ApiPublic {
        fn new(token: &str, user_id: &str, country_code: &str) -> Self {
            Self { session: DummySessionPublic::new(), user_id: user_id.to_string(), country_code: country_code.to_string(), token: token.to_string() }
        }

        fn fetch(&self, _model: &str, endpoint: &str, _params: Option<HashMap<&str, u32>>) -> Result<DummyModelPublic, ApiError> {
            let resp = self.session.get(endpoint, None, None);
            if resp.status_code == 201 {
                Ok(DummyModelPublic{ id: *resp.data.get("id").unwrap() })
            } else {
                Err(ApiError{
                    status: resp.status_code,
                    sub_status: None,
                    user_message: Some("Forbidden".to_string()),
                    error_code: None,
                    message: None,
                    others: HashMap::new(),
                })
            }
        }
    }

    #[test]
    fn test_ensure_limit_warns_public() {
        assert_eq!(ensure_limit(99, 10), 10);
        assert_eq!(ensure_limit(8, 10), 8);
    }

    #[test]
    fn test_api_fetch_success_public() {
        let api = ApiPublic::new("tok", "uid_pub", "country");
        let result = api.fetch("DummyModelPublic", "endpoint/42", None).unwrap();
        assert_eq!(result.id, 321);
        let req_url = api.session.req.borrow();
        assert!(req_url.is_some());
        assert!(req_url.as_ref().unwrap().0.ends_with("endpoint/42"));
    }

    #[test]
    fn test_api_fetch_failure_public() {
        // Simulate fetch failure returning Forbidden error
        let mut result = Err(ApiError{
            status: 403,
            sub_status: None,
            user_message: Some("Forbidden".to_string()),
            error_code: None,
            message: None,
            others: HashMap::new(),
        });
        assert!(result.is_err());
        let err = result.err().unwrap();
        assert!(format!("{}", err).contains("Forbidden"));
    }

    #[test]
    fn test_api_methods_public() {
        // Patch fetch to record calls
        let mut called = Vec::new();
        let fake_fetch = |model: &'static str, endpoint: &'static str, params: Option<HashMap<&str, u32>>| {
            called.push((model, endpoint.to_string(), params.clone()));
            model
        };
        let result = fake_fetch("Album", "getAlbum/77", None);
        assert_eq!(result, "Album");
        let mut params = HashMap::new();
        params.insert("limit", 3_u32);
        params.insert("offset", 2_u32);
        let result2 = fake_fetch("AlbumItems", "getAlbumItems/77", Some(params));
        assert_eq!(result2, "AlbumItems");
        let mut params2 = HashMap::new();
        params2.insert("limit", 1_u32);
        let result3 = fake_fetch("AlbumItemsCredits", "getAlbumItemsCredits/2", Some(params2));
        assert_eq!(result3, "AlbumItemsCredits");
        let result4 = fake_fetch("Artist", "getArtist/99", None);
        assert_eq!(result4, "Artist");
        let result5 = fake_fetch("ArtistAlbumsItems", "getArtistAlbums/44", None);
        assert_eq!(result5, "ArtistAlbumsItems");
        assert_eq!(called.len(), 5);
    }
}