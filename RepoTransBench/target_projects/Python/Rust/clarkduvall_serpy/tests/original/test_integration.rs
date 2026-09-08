use crate::serpy::*;
use crate::obj::Obj;
use std::collections::HashMap;

struct DummyObj {
    pub a: i32,
    pub b: i32,
    pub c: Option<i32>,
    pub method_val: i32,
}
impl DummyObj {
    fn new(a: i32, b: i32, c: Option<i32>, method_val: i32) -> Self {
        Self { a, b, c, method_val }
    }
    fn meth(&self) -> i32 {
        self.method_val
    }
}

#[test]
fn test_simple_serialization() {
    struct Ex;
    impl Ex {
        fn to_value(&self, o: &DummyObj) -> HashMap<String, serde_json::Value> {
            let mut map = HashMap::new();
            map.insert("a".to_string(), serde_json::json!(o.a));
            map.insert("b".to_string(), serde_json::json!(o.b));
            map
        }
    }
    let o = DummyObj::new(4, 5, None, 0);
    let result = Ex.to_value(&Ex, &o);
    assert_eq!(result.get("a"), Some(&serde_json::json!(4)));
    assert_eq!(result.get("b"), Some(&serde_json::json!(5)));
}

#[test]
fn test_method_and_custom_labels() {
    struct Ex;
    impl Ex {
        fn get_foo(&self, o: &DummyObj) -> i32 {
            o.method_val
        }
        fn to_value(&self, o: &DummyObj) -> HashMap<String, serde_json::Value> {
            let mut map = HashMap::new();
            map.insert("maybe".to_string(), serde_json::json!(self.get_foo(o)));
            map
        }
    }
    let o = DummyObj::new(0, 0, None, 42);
    let ex = Ex;
    let data = ex.to_value(&o);
    assert!(data.contains_key("maybe"));
    assert_eq!(data.get("maybe"), Some(&serde_json::json!(42)));
}

#[test]
fn test_dict_serializer() {
    struct DSer;
    impl DSer {
        fn to_value(&self, d: &std::collections::HashMap<&str, i32>) -> HashMap<String, serde_json::Value> {
            let mut map = HashMap::new();
            map.insert("x".to_string(), serde_json::json!(*d.get("x").unwrap()));
            map.insert("y".to_string(), serde_json::json!(*d.get("y").unwrap()));
            map
        }
    }
    let mut d = HashMap::new();
    d.insert("x", 10);
    d.insert("y", 21);
    let result = DSer.to_value(&DSer, &d);
    assert_eq!(result.get("x"), Some(&serde_json::json!(10)));
    assert_eq!(result.get("y"), Some(&serde_json::json!(21)));
}

#[test]
fn test_edge_cases_and_repr() {
    struct Example;
    impl Example {
        fn to_value(&self, o: &Obj) -> HashMap<String, serde_json::Value> {
            let mut map = HashMap::new();
            map.insert("foo".to_string(), serde_json::json!(o.foo.clone().unwrap_or("".to_string())));
            map
        }
    }
    let o = Obj::with_foo("edgecase");
    let ex = Example;
    let _repr_str = format!("{:?}", ex.to_value(&o));
    assert!(_repr_str.contains("foo"));
}