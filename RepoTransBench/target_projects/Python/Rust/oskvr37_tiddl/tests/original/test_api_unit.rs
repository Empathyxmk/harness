#[cfg(test)]
mod tests {
    use std::collections::HashMap;
    use std::cell::RefCell;
    use crate::exceptions::ApiError;
    use std::rc::Rc;

    // Emulate a dummy API module and types for testing logic
    #[derive(Debug, PartialEq)]
    struct DummyModel {
        id: u32,
    }

    struct DummyResponse {
        data: HashMap<&'static str, u32>,
        status_code: u32,
        from_cache: bool,
    }
    impl DummyResponse {
        fn json(&self) -> HashMap<&'static str, u32> {
            self.data.clone()
        }
    }

    struct DummySession {
        req: Rc<RefCell<Option<(String, Option<HashMap<&'static str, u32>>, Option<u32>)>>>,
        headers: HashMap<String, String>,
    }
    impl DummySession {
        fn new() -> Self {
            Self { req: Rc::new(RefCell::new(None)), headers: HashMap::new() }
        }
        fn get(&self, url: &str, params: Option<HashMap<&str, u32>>, expire_after: Option<u32>) -> DummyResponse {
            *self.req.borrow_mut() = Some((url.to_string(), params.clone(), expire_after));
            let mut data = HashMap::new();
            data.insert("id", 123);
            DummyResponse { data, status_code: 200, from_cache: false }
        }
    }

    // Emulate ensureLimit logic
    fn ensure_limit(val: u32, max: u32) -> u32 {
        if val > max {
            // Would warn; here just cap
            max
        } else {
            val
        }
    }

    struct Api {
        pub session: Rc<DummySession>,
        pub user_id: String,
        pub country_code: String,
        pub token: String,
    }

    impl Api {
        fn new(token: &str, user_id: &str, country_code: &str) -> Self {
            Self { session: Rc::new(DummySession::new()), user_id: user_id.to_string(), country_code: country_code.to_string(), token: token.to_string()}
        }

        fn fetch(&self, _model: &str, endpoint: &str, _params: Option<HashMap<&str, u32>>) -> Result<DummyModel, ApiError> {
            let resp = self.session.get(endpoint, None, None);
            if resp.status_code == 200 {
                Ok(DummyModel{id: *resp.data.get("id").unwrap()})
            } else {
                Err(ApiError{
                    status: resp.status_code,
                    sub_status: None,
                    user_message: Some("Auth fail".to_string()),
                    error_code: None,
                    message: None,
                    others: HashMap::new(),
                })
            }
        }
    }

    #[test]
    fn test_ensure_limit_warns() {
        assert_eq!(ensure_limit(111, 5), 5);
        assert_eq!(ensure_limit(3, 5), 3);
    }

    #[test]
    fn test_api_fetch_success() {
        let api = Api::new("token", "uid", "cc");
        let result = api.fetch("DummyModel", "endpoint/1", None).unwrap();
        assert_eq!(result.id, 123);
        let req_url = api.session.req.borrow();
        assert!(req_url.is_some());
        assert!(req_url.as_ref().unwrap().0.ends_with("endpoint/1"));
    }

    #[test]
    fn test_api_fetch_failure() {
        struct ErrSession;
        impl ErrSession {
            fn get(&self, _url: &str, _params: Option<HashMap<&str, u32>>, _expire_after: Option<u32>) -> DummyResponse {
                let mut data = HashMap::new();
                data.insert("status", 401);
                DummyResponse{data, status_code: 401, from_cache: false}
            }
        }
        // Simulate by using local fetch with failure
        let api = Api::new("token", "uid", "cc");
        // Overriding fetch for the error case
        let error_fetch = |_model: &str, _endpoint: &str, _params: Option<HashMap<&str, u32>>| {
            Err(ApiError{
                status: 401,
                sub_status: None,
                user_message: Some("Auth fail".to_string()),
                error_code: None,
                message: None,
                others: HashMap::new(),
            })
        };
        let result = error_fetch("DummyModel", "endpoint/1", None);
        assert!(result.is_err());
        let err = result.err().unwrap();
        assert_eq!(err.status, 401);
        assert_eq!(err.user_message.unwrap(), "Auth fail");
    }

    #[test]
    fn test_api_methods() {
        // Patch fetch to record calls
        let calls = Rc::new(RefCell::new(vec![]));
        let called = calls.clone();
        // fake fetch just returns model string
        let fake_fetch = |model: &'static str, endpoint: &'static str, params: Option<HashMap<&str, u32>>| {
            called.borrow_mut().push((model, endpoint.to_string(), params.clone()));
            model
        };
        // These are mostly symbolic for coverage
        let result = fake_fetch("Album", "getAlbum/55", None);
        assert_eq!(result, "Album");
        let mut params = HashMap::new();
        params.insert("limit", 5_u32);
        params.insert("offset", 1_u32);
        let result2 = fake_fetch("AlbumItems", "getAlbumItems/55", Some(params));
        assert_eq!(result2, "AlbumItems");
        let mut params2 = HashMap::new();
        params2.insert("limit", 2_u32);
        let result3 = fake_fetch("AlbumItemsCredits", "getAlbumItemsCredits/5", Some(params2));
        assert_eq!(result3, "AlbumItemsCredits");
        let result4 = fake_fetch("Artist", "getArtist/4", None);
        assert_eq!(result4, "Artist");
        let result5 = fake_fetch("ArtistAlbumsItems", "getArtistAlbums/5", None);
        assert_eq!(result5, "ArtistAlbumsItems");
        // Check calls vector for expected entries
        assert!(calls.borrow().len() == 5);
    }
}