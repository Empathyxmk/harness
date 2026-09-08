use crate::obj::Obj;
use std::collections::HashMap;

struct TestSerializer1;
impl TestSerializer1 {
    fn to_value(&self, o: &Obj) -> HashMap<String, String> {
        let mut map = HashMap::new();
        map.insert("foo".to_string(), o.foo.clone().unwrap_or_default());
        map
    }
}

struct TestSerializer2;
impl TestSerializer2 {
    fn to_value(&self, o: &Obj) -> HashMap<String, i32> {
        let mut map = HashMap::new();
        map.insert("bar".to_string(), o.bar.clone().and_then(|s| s.parse::<i32>().ok()).unwrap_or(0));
        map
    }
}

struct TestSerializer3;
impl TestSerializer3 {
    fn to_value(&self, o: &Obj) -> HashMap<String, String> {
        let mut map = HashMap::new();
        map.insert("special".to_string(), o.foo.clone().unwrap_or_default().to_uppercase());
        map
    }
}

struct TestSerializer4;
impl TestSerializer4 {
    fn to_value(&self, o: &Obj) -> HashMap<String, Option<String>> {
        let mut map = HashMap::new();
        // bar is missing
        map.insert("bar".to_string(), o.bar.clone());
        map
    }
}

#[test]
fn test_str_field() {
    let o = Obj::with_foo("differentstr");
    let data = TestSerializer1.to_value(&TestSerializer1, &o);
    assert_eq!(data.get("foo"), Some(&"differentstr".to_string()));
}

#[test]
fn test_int_field() {
    let mut o = Obj::default();
    o.bar = Some("100".to_string());
    let data = TestSerializer2.to_value(&TestSerializer2, &o);
    assert_eq!(data.get("bar"), Some(&100));
}

#[test]
fn test_method_field() {
    let o = Obj::with_foo("public");
    let data = TestSerializer3.to_value(&TestSerializer3, &o);
    assert_eq!(data.get("special"), Some(&"PUBLIC".to_string()));
}

#[test]
fn test_missing_value_field() {
    let o = Obj::default(); // bar is missing
    let data = TestSerializer4.to_value(&TestSerializer4, &o);
    assert_eq!(data.get("bar"), Some(&None));
}