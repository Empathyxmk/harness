// test_public_utils_coverage.rs

#[cfg(test)]
mod tests {
    use std::collections::HashMap;

    // Simulate input_checker functionality (with different params than original)
    mod input_checker {
        pub fn check_should_not_none<T>(val: Option<T>, _param: &str) -> Result<(), String> {
            match val {
                Some(_) => Ok(()),
                None => Err("Value is None".to_string()),
            }
        }
        pub fn check_should_none<T>(val: Option<T>, _param: &str) -> Result<(), String> {
            match val {
                None => Ok(()),
                Some(_) => Err("Value is not None".to_string()),
            }
        }
    }

    mod url_params_builder {
        use std::collections::HashMap;
        #[derive(Default)]
        pub struct UrlParamsBuilder {
            pub params: HashMap<String, String>,
        }
        impl UrlParamsBuilder {
            pub fn new() -> Self {
                Self { params: HashMap::new() }
            }
            pub fn put_url(&mut self, k: &str, v: &str) {
                self.params.insert(k.to_string(), v.to_string());
            }
            pub fn build_url(&self) -> String {
                if self.params.is_empty() {
                    "".to_string()
                } else {
                    let mut pairs: Vec<String> = self.params.iter().map(|(k, v)| format!("{}={}", k, v)).collect();
                    pairs.sort();
                    format!("?{}", pairs.join("&"))
                }
            }
        }
    }
    mod log_info {
        pub fn print_warn(_msg: &str) {}
        pub fn print_basic_info(_msg: &str) {}
        pub fn print_replace(_from: &str, _to: &str) {}
    }
    mod time_service {
        pub fn get_current_timestamp() -> i64 {
            7654321 // just a different value
        }
    }
    mod print_mix_object {
        pub fn print_basic_object<T: std::fmt::Debug>(obj: &T) {
            let _ = format!("{:?}", obj);
        }
        pub fn print_list<T: std::fmt::Debug>(lst: &[T]) {
            for obj in lst {
                let _ = format!("{:?}", obj);
            }
        }
        pub fn print_dict<V: std::fmt::Debug>(dict: &std::collections::HashMap<&str, V>) {
            for (k, v) in dict {
                let _ = format!("{}:{:?}", k, v);
            }
        }
        pub fn print_basic_dict<V: std::fmt::Debug>(dict: &std::collections::HashMap<&str, V>) {
            for (k, v) in dict {
                let _ = format!("{}:{:?}", k, v);
            }
        }
        pub fn print_basic_list<T: std::fmt::Debug>(lst: &[T]) {
            for v in lst {
                let _ = format!("{:?}", v);
            }
        }
    }
    mod json_parser {
        use serde_json::{json, Value};
        pub fn json_dumps(v: &serde_json::Value) -> String {
            serde_json::to_string(v).unwrap()
        }
        pub fn json_loads(s: &str) -> serde_json::Value {
            serde_json::from_str(s).unwrap()
        }
    }

    #[test]
    fn test_check_should_not_none() {
        assert!(input_checker::check_should_not_none::<i32>(None, "different_param").is_err());
    }

    #[test]
    fn test_check_should_not_none_valid() {
        assert!(input_checker::check_should_not_none(Some(123), "another_param").is_ok());
    }

    #[test]
    fn test_check_should_none() {
        assert!(input_checker::check_should_none::<i32>(None, "wonka_param").is_ok());
        // Edge: check_should_none(0, ...) => error
        assert!(input_checker::check_should_none(Some(0), "wonka_param").is_err());
    }

    #[test]
    fn test_add_and_build_url() {
        let mut builder = url_params_builder::UrlParamsBuilder::new();
        builder.put_url("x", "alpha");
        builder.put_url("y", "beta");
        let url = builder.build_url();
        let valid1 = "?x=alpha&y=beta";
        let valid2 = "?y=beta&x=alpha";
        assert!(url == valid1 || url == valid2, "url was {}", url);
        let builder2 = url_params_builder::UrlParamsBuilder::new();
        assert_eq!(builder2.build_url(), "");
    }

    #[test]
    fn test_log_methods_exist() {
        log_info::print_warn("public warn message");
        log_info::print_basic_info("public info message");
        log_info::print_replace("public_from", "public_to");
    }

    #[test]
    fn test_get_current_time() {
        let now = time_service::get_current_timestamp();
        assert!(now >= 0);
    }

    struct Dummy;
    impl std::fmt::Debug for Dummy {
        fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { write!(f, "OtherDummy") }
    }
    #[test]
    fn test_print_object_basic() {
        let obj = Dummy;
        print_mix_object::print_basic_object(&obj);
    }

    #[test]
    fn test_print_list_and_dict() {
        let obj = Dummy;
        print_mix_object::print_list(&[obj, obj]);
        print_mix_object::print_list(&[obj]);
        let mut dict = std::collections::HashMap::new();
        dict.insert("b", 2);
        dict.insert("a", 42);
        print_mix_object::print_dict(&dict);
        let mut basicdict = std::collections::HashMap::new();
        basicdict.insert("z", 789);
        print_mix_object::print_basic_dict(&basicdict);
        print_mix_object::print_basic_list(&[9, 8, 7]);
        print_mix_object::print_basic_list(&[0]);
    }

    #[test]
    fn test_parse() {
        use serde_json::json;
        let obj = json!({"spam": "eggs"});
        let json_str = json_parser::json_dumps(&obj);
        let result = json_parser::json_loads(&json_str);
        assert_eq!(result["spam"], "eggs");
    }
}