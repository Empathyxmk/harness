use crate::obj::Obj;
use std::collections::HashMap;

struct IntegrationPublicSerializer;

impl IntegrationPublicSerializer {
    fn get_c(o: &Obj) -> String {
        let b = o.b.clone().unwrap_or_default();
        b.clone() + &b
    }
    fn get_d(o: &Obj) -> Option<i32> {
        o.d
    }
    fn to_value(&self, o: &Obj) -> HashMap<String, serde_json::Value> {
        let mut map = HashMap::new();
        map.insert("a".to_string(), serde_json::json!(o.a.unwrap_or(0)));
        map.insert("b".to_string(), serde_json::json!(o.b.clone().unwrap_or_default()));
        map.insert("c".to_string(), serde_json::json!(Self::get_c(o)));
        map.insert("d".to_string(), match Self::get_d(o) {
            Some(v) => serde_json::json!(v),
            None => serde_json::Value::Null,
        });
        map
    }
    fn to_value_many(&self, objs: &[Obj]) -> Vec<HashMap<String, serde_json::Value>> {
        objs.iter().map(|o| self.to_value(o)).collect()
    }
}

#[test]
fn test_all_fields() {
    let o = Obj::with_ab(99, "foo", Some(255));
    let data = IntegrationPublicSerializer.to_value(&IntegrationPublicSerializer, &o);
    assert_eq!(data.get("a"), Some(&serde_json::json!(99)));
    assert_eq!(data.get("b"), Some(&serde_json::json!("foo")));
    assert_eq!(data.get("c"), Some(&serde_json::json!("foofoo")));
    assert_eq!(data.get("d"), Some(&serde_json::json!(255)));
}

#[test]
fn test_missing_field() {
    let o = Obj::with_ab(44, "echo", None); // d is missing
    let data = IntegrationPublicSerializer.to_value(&IntegrationPublicSerializer, &o);
    assert_eq!(data.get("a"), Some(&serde_json::json!(44)));
    assert_eq!(data.get("b"), Some(&serde_json::json!("echo")));
    assert_eq!(data.get("c"), Some(&serde_json::json!("echoecho")));
    assert_eq!(data.get("d"), Some(&serde_json::Value::Null));
}

#[test]
fn test_list_many() {
    let objs = vec![
        Obj::with_ab(8, "a", None),
        Obj::with_ab(9, "Xx", Some(777)),
    ];
    let result = IntegrationPublicSerializer.to_value_many(&IntegrationPublicSerializer, &objs);
    let expected = vec![
        [
            ("a".to_string(), serde_json::json!(8)),
            ("b".to_string(), serde_json::json!("a")),
            ("c".to_string(), serde_json::json!("aa")),
            ("d".to_string(), serde_json::Value::Null),
        ].into_iter().collect(),
        [
            ("a".to_string(), serde_json::json!(9)),
            ("b".to_string(), serde_json::json!("Xx")),
            ("c".to_string(), serde_json::json!("XxXx")),
            ("d".to_string(), serde_json::json!(777)),
        ].into_iter().collect(),
    ];
    assert_eq!(result, expected);
}