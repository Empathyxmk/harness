use crate::obj::Obj;
use std::collections::HashMap;

struct AnotherPublicSerializer;
impl AnotherPublicSerializer {
    fn to_value(&self, o: &Obj) -> HashMap<String, serde_json::Value> {
        let mut map = HashMap::new();
        map.insert("name".to_string(), serde_json::json!(o.name.clone().unwrap_or_default()));
        map.insert("value".to_string(), serde_json::json!(o.value.unwrap_or(0)));
        map
    }
    fn to_value_many(&self, objs: &[Obj]) -> Vec<HashMap<String, serde_json::Value>> {
        objs.iter().map(|o| self.to_value(o)).collect()
    }
}

struct MethodPublicSerializer;
impl MethodPublicSerializer {
    fn get_double(o: &Obj) -> String {
        o.foo.clone().unwrap_or_default().repeat(2)
    }
    fn to_value(&self, o: &Obj) -> HashMap<String, serde_json::Value> {
        let mut map = HashMap::new();
        map.insert("foo".to_string(), serde_json::json!(o.foo.clone().unwrap_or_default()));
        map.insert("double".to_string(), serde_json::json!(Self::get_double(o)));
        map
    }
    fn to_value_many(&self, objs: &[Obj]) -> Vec<HashMap<String, serde_json::Value>> {
        objs.iter().map(|o| self.to_value(o)).collect()
    }
}

#[test]
fn test_serializer_basic() {
    let o = Obj::with_name_value("other", 13);
    let data = AnotherPublicSerializer.to_value(&AnotherPublicSerializer, &o);
    assert_eq!(data.get("name"), Some(&serde_json::json!("other")));
    assert_eq!(data.get("value"), Some(&serde_json::json!(13)));
}

#[test]
fn test_serializer_many() {
    let objects = vec![
        Obj::with_name_value("x", 2),
        Obj::with_name_value("y", 7),
    ];
    let data = AnotherPublicSerializer.to_value_many(&AnotherPublicSerializer, &objects);
    let expected = vec![
        [("name".to_string(), serde_json::json!("x")), ("value".to_string(), serde_json::json!(2))].into_iter().collect(),
        [("name".to_string(), serde_json::json!("y")), ("value".to_string(), serde_json::json!(7))].into_iter().collect(),
    ];
    assert_eq!(data, expected);
}

#[test]
fn test_method_serializer() {
    let o = Obj::with_foo("hello");
    let data = MethodPublicSerializer.to_value(&MethodPublicSerializer, &o);
    assert_eq!(data.get("foo"), Some(&serde_json::json!("hello")));
    assert_eq!(data.get("double"), Some(&serde_json::json!("hellohello")));
}

#[test]
fn test_method_serializer_many() {
    let objects = vec![
        Obj::with_foo("abc"),
        Obj::with_foo("de"),
    ];
    let data = MethodPublicSerializer.to_value_many(&MethodPublicSerializer, &objects);
    let expected = vec![
        [("foo".to_string(), serde_json::json!("abc")), ("double".to_string(), serde_json::json!("abcabc"))].into_iter().collect(),
        [("foo".to_string(), serde_json::json!("de")), ("double".to_string(), serde_json::json!("dede"))].into_iter().collect(),
    ];
    assert_eq!(data, expected);
}